from bs4 import BeautifulSoup
from crawler.linkExtracter import linkExtracter
# from config.seedUrl import url_queue # create copy
import config.seedUrl

def parser(response):
    content = []
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find("title")
    if title:
        content.append(title.get_text(strip=True))
    
    meta = soup.find("meta", attrs={"name": "description"})
    if meta:
        content.append(meta.get("content", ""))

    links, count = linkExtracter(soup, response)
    
    for link in links:
        # url_queue.append(link)
        config.seedUrl.url_queue.append(link)
        

    return {
        "title": title,
        "description": meta,
        "content": content,
        "count": count
    }