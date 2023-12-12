import multiprocessing
from concurrent.futures import ThreadPoolExecutor

import requests
from urllib.robotparser import RobotFileParser
from typing import Iterable

from bs4 import BeautifulSoup


class UrlsHandler:
    def __init__(self, domain: str) -> None:
        self.domain = domain

    def url_filter(self, url: str) -> bool:
        if url:
            return url.startswith(self.domain) or url.startswith("/")
        return False

    def get_all_links(self, url: str) -> Iterable[str]:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        links = set()
        links_elements = soup.find_all("a")
        for link_element in links_elements:
            link = link_element.get("href")
            if self.url_filter(link):
                if link.startswith("/"):
                    link = f"{self.domain}{link}"
                links.add(link)

        return links
    
    @staticmethod
    def get_domain_from_url(url: str) -> str:
        domain_parts = url.split("/")[:3]
        domain = "/".join(domain_parts)
        return domain


class RobotsTxt:
    def __init__(self, domain: str) -> None:
        self.robots_txt = RobotFileParser()
        self.robots_txt.set_url(f"{domain}/robots.txt")
        self.robots_txt.read()


class Crawler:
    def __init__(self, url: str, websites_limit: int = 25, user_agent: str = "*",) -> None:
        self.url = url
        self.domain = UrlsHandler.get_domain_from_url(url)
        self.user_agent = user_agent
        self.websites_limit = websites_limit
        self.urls_handler = UrlsHandler(self.domain)
        self.robots_txt = RobotsTxt(self.domain)
        self.graph = dict()

    def crawl(self):
        websites_counter = 0
        urls = [self.url, ]
        visited_urls = set()

        while urls and websites_counter < self.websites_limit:
            url = urls[0]
            if url not in visited_urls:
                visited_urls.add(url)
                links = self.urls_handler.get_all_links(url)
                print(url)
                self.graph[url] = links
                urls.pop(0)
                urls.extend(links)
                websites_counter += 1
        print(f"{websites_counter} sites were visited")
        print(f"{self.graph}")

# https://docs.python.org https://bntu.by
