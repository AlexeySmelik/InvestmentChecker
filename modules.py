import requests
import config
from DBoperator import insert_ticker, get_stocks, delete_stocks
from bs4 import BeautifulSoup as BS
from functools import lru_cache


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
    

    def get_user_stocks(self):
        return get_stocks(self.chat_id)


    def try_add_stock(self, stock):
        if not stock.is_it_correct():
            return False
        insert_ticker(self.chat_id, stock.ticker, stock.needed_price)
        return True
    

    def delete_user_stocks(self, stocks):
        correct_tickers = list(filter(None, map(lambda x: Stock(x).ticker, stocks)))
        delete_stocks(self.chat_id, correct_tickers)
        

class Stock:
    def __init__(self, name, price = 54):
        self.name = name.upper()
        self.needed_price = price
        self.ticker = Stock.get_ticker(self.name)


    @lru_cache
    def get_ticker(name):        
        url = f"https://google.com/search?q={name}+акция"
        headers = {"user-agent" : config.user_agent}
        resp = requests.get(url, headers=headers)
        soup = BS(resp.content, "html.parser")
        res = soup.select(config.ticker)
        return res[0].text if res else None


    def is_it_correct(self):
        return self.ticker