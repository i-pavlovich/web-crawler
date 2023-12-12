import re
import requests
from typing import Iterable
from collections import defaultdict

from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url: str) -> None:
        self.urls = list(url)
        self.__visited_urls = defaultdict(lambda: None)

    def __extract_links(self, soup: BeautifulSoup) -> dict[str, int]:
        links = defaultdict(lambda: 0)

        # Добавить фильтрацию ссылок (+ приоритет)
        link_elements = soup.find_all("a")
        for link_element in link_elements:
            link = link_element.get("href")
            if link not in ["#", None, ]:
                links[link] += 1

        links = sorted(links.items(), key=lambda x: links[x[0]], reverse=True)
        links = {key: value for key, value in links}
        return links

    def __extract_text_data(self, soup: BeautifulSoup) -> Iterable:
        text_content = []

        p_tags = soup.find_all("p")
        for p_tag in p_tags:
            text_content.append(p_tag.text.strip())

        return text_content

    def __extract_headers_text(self, soup: BeautifulSoup) -> Iterable:
        headers_content = []

        headers = soup.find_all("^h[1-6]$")
        for header in headers:
            headers_content.append(header.text.strip())

        return headers_content

    def get_data_from_url(self, url: str) -> dict[str, Iterable]:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # return {
        #     "links": self.__extract_links(soup),
        #     "headers": self.__extract_headers_text(soup),
        #     "text_data": self.__extract_text_data(soup),
        # }
        return self.__extract_links(soup)

    def read_robots_txt(self, domain: str):
        response = requests.get(f"{domain}/robots.txt", verify=False)
        return response.text
    
    def get_links(self, url: str) -> dict[str, int]:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        links = defaultdict(lambda: 0)

        # Добавить фильтрацию ссылок (+ приоритет)
        link_elements = soup.find_all("a")
        for link_element in link_elements:
            link = link_element.get("href")
            if link not in ["#", None, ]:
                links[link] += 1

        links = sorted(links.items(), key=lambda x: links[x[0]], reverse=True)
        links = {key: value for key, value in links}
        return links

    def run(self, limit: int = 100):
        counter = 1

        while self.urls and counter <= limit:
            url = self.urls[0]

            if self.__visited_urls[url] == None:
                self.__visited_urls[url] = counter
                links = self.get_links(url)
                self.urls.pop(0)
                self.urls += links.keys()
            else:
                continue
            counter += 1
        
        print(self.__visited_urls)

