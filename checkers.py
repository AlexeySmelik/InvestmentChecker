import requests
from bs4 import BeautifulSoup as BS
from functools import lru_cache
from config import user_agent


class StockChecker():
    @lru_cache
    def get_ticker(self, name):        
        return self.__get_info(name, 'g-card-section:last-child > div:not([aria-level]) > div:last-child > div > span:last-child')


    def get_cost(self, name):        
        return self.__get_info(name, 'g-card-section:last-child > div:not([aria-level]) > div > span > span > span')


    @staticmethod
    def __get_info(name, selector):
        url = f"https://google.com/search?q={name}+акция"
        headers = {"user-agent" : user_agent}
        resp = requests.get(url, headers=headers)
        soup = BS(resp.content, "html.parser")
        res = soup.select(selector)
        return res[0].text if res else None
