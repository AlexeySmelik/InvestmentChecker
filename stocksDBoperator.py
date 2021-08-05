import requests
import config
from bs4 import BeautifulSoup as BS
from functools import lru_cache
from Tables import * 


@lru_cache
def get_ticker(name):        
    url = f"https://google.com/search?q={name}+акция"
    headers = {"user-agent" : config.user_agent}
    resp = requests.get(url, headers=headers)
    soup = BS(resp.content, "html.parser")
    res = soup.select('g-card-section:last-child > div:not([aria-level]) > div:last-child > div > span:last-child')
    return res[0].text if res else None


def get_user_stocks(chat_id):
     return Stocks.select(Stocks.ticker, Stocks.needed_price).where(Stocks.chat_id == chat_id).execute()


def try_add_stock(chat_id, name, needed_price):
    ticker = get_ticker(name)
    if not ticker:
        return False
    Stocks.get_or_create(chat_id = chat_id, ticker = ticker)
    Stocks.set_by_id((chat_id, ticker), {Stocks.needed_price : needed_price})
    return True


def delete_user_stocks(chat_id, names):
    correct_tickers = list(filter(None, map(lambda name: get_ticker(name), names)))
    for ticker in correct_tickers:
        Stocks.delete().where(Stocks.chat_id == chat_id, Stocks.ticker == ticker).execute()


def main():
    Stocks.create_table()


if __name__ == "__main__":
    main()