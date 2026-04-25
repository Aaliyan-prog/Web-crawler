# URL Queue Management
import requests
# from config.seedUrl import url_queue
import crawler.robots_handling as robot
import config.seedUrl
from crawler.parser import parser
from collections import deque

def main():
    print("Welcome to crawler")

    max_pages = 6
    visited = set()
    crawled_pages = []

    # Use a deque for O(1) pops from the left
    queue = deque(config.seedUrl.url_queue)

    crawler = input("Do you want to crawl[yes/no]: ")

    if crawler == "yes":
        header = {
            "User-agent": (
                "Mozilla/5.0 (X11; Linux x84_64) "
                "AppleWebkit/537.36 (KHTML, like Gecko) "
                "Chrome 120.0.0.0 Safari/537.36"
            ),
            "Accept-language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive"
        }

        while queue and len(visited) < max_pages:
            urls = queue.popleft() # Get the next URL
            
            if urls in visited:
                continue

            try:
                if len(visited) >= max_pages:
                    print(f"Reached max pages: {max_pages}")
                    break
                
                if not robot.robots_handler(urls, header):
                    print(f"Skipping {urls} - Disallowing by Robots.txt")
                    continue

                response = requests.get(urls, headers=header, timeout=10)

                status_code = response.status_code
                    
                if status_code == 200:
                    meta_data = parser(response)

                    if meta_data["count"] == 0:
                        print(f"Skipping {urls} no <a> tags found")
                        continue

                    visited.add(urls)

                    for link in config.seedUrl.url_queue:
                        if link not in visited:
                            queue.append(link)
                

                    crawled_pages.append({
                        "url": urls,
                        "title": meta_data["title"],
                        "description": meta_data["description"],
                        "content": meta_data["content"],
                        "count": meta_data["count"]
                    })

                else:
                    print("status code", status_code)

            except requests.exceptions.Timeout:
                print(f"Timeout {urls}")
                continue
            except requests.exceptions.ConnectionError:
                print(f"Connection Error {urls}")
                continue
            except Exception as e:
                print(f"Error: {urls} - {e}")
                continue
        

        print("Crawled completed")
        print(f"Pages Crawled: {len(visited)}")
        print(f"pages in queue: {len(config.seedUrl.url_queue)}")
        print(f"Data Collected {len(crawled_pages)}")
    else:
        print("maybe next time!")
        return
