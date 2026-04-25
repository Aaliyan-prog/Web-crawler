# fetcher
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def linkExtracter(soup, response):
    new_urls = set();

    base_url = response.url

    a_tags = soup.find_all("a")

    print(f"Found: {len(a_tags)} <a> tags | url {response.url} | status-code: {response.status_code}")

    if not a_tags:
        return [], len(a_tags)

    if a_tags:
        for link in a_tags:
            href = link.get("href")
            
            if not href:
                continue

            if href.startswith(("#", "mailto:", "javascript:")):
                continue

            clean_url = urljoin(base_url, href)
            new_urls.add(clean_url)

        with open("./storage/new-url.txt", "a") as file:
            for url in new_urls:
                file.write(url + "\n")

        
    print("url fetched successfully for: ", response.url)
    return list(new_urls), len(a_tags)