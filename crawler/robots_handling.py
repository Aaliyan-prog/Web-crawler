# robot_handler
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import requests

robot_cache = {}

def robots_handler(url, header):
    urlsplit = urlparse(url)
    protocol = urlsplit.scheme
    domain = urlsplit.netloc
    robotsurl = f"{protocol}://{domain}/robots.txt"

    if domain in robot_cache:
        rp = robot_cache[domain]

        if rp is None:
            return True
        return rp.can_fetch("*", url)

    try:
        response = requests.get(robotsurl, headers=header, timeout=10)
        robotStatus = response.status_code
    
        if robotStatus == 200:
            rp = RobotFileParser()
            rp.parse(response.text.splitlines())
            robot_cache[domain] = rp
            return rp.can_fetch("*", url)
        elif robotStatus == 403:
            robot_cache[domain] = None
            return False
        else:
            robot_cache[domain] = None
            return False

    except Exception as e:
        print(f"Error fetching robots.txt for {domain}: {e}")
        return True