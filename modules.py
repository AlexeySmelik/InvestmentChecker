import requests
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
        correct_stocks = list(filter(None, map(lambda x: Stock(x).ticker, stocks)))
        delete_stocks(self.chat_id, correct_stocks)
        

class Stock:
    def __init__(self, name, price = 54):
        self.name = name.upper()
        self.needed_price = price
        self.ticker = Stock.get_ticker(self.name)


    @lru_cache
    def get_ticker(name):
        url = f'https://yandex.ru/search/?text="{name} акция"'
        headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}
        html_doc = requests.get(url, headers=headers).content
        soup = BS(html_doc, 'html.parser')
        result = soup.find('span', {'class' : 'StocksHeader-Ticker'})
        return result[0].get_text() if len(result) == 0 else None


    def is_it_correct(self):
        return self.ticker