import time
import urllib3
import random

# Disable all warnings about SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import flet as ft
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx

from src.crawler import Crawler
from src.interface import main


if __name__ == "__main__":    
    crawler = Crawler("https://flet.dev/docs/controls/buttons", websites_limit=10)
    start_time = time.time()
    crawler.crawl()
    print(f"{time.time() - start_time:.2f} sec")

    G = nx.Graph()
    for node in crawler.graph.keys():
        G.add_node(node)
    for key, value in crawler.graph.items():
        for node in value:
            G.add_edge(key, node)
    seed = random.randint(1, 77)
    pos = nx.layout.spring_layout(G, seed=seed)
    nx.drawing.nx_pylab.draw(G, pos, with_labels=True)
    plt.show()

    # ft.app(target=main, view=ft.WEB_BROWSER)

    # Интерфейс
    # Нормализация ссылок
    # Запись в бд
    # Выбор текста (заголовков)
    # Поиск ключевых слов
    # SSL?
    # Websites limit

    # for link in link_elements:
    #     print(link.get("href"))
