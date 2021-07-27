from threading import Event, Thread
from Tables import * 
import requests
from bs4 import BeautifulSoup as BS


def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set


def check_tickers(message):    
    tickers = Stocks.select(Stocks.ticker).distinct()
    for ticker in tickers:  # chunked !! api model
        stocks = pop_stocks(ticker.ticker)
        message(stocks)
        

def pop_stocks(ticker):
    close = get_cost(ticker).replace(',','.').encode('ascii', 'ignore')
    stocks = Stocks.select().where(Stocks.ticker == ticker and Stocks.needed_price < float(close)).execute()
    Stocks.delete().where(Stocks.ticker == ticker and Stocks.needed_price < float(close)).execute()
    return stocks


def get_cost(name):        
    url = f"https://google.com/search?q={name}+акция"
    headers = {"user-agent" : config.user_agent}
    resp = requests.get(url, headers=headers)
    soup = BS(resp.content, "html.parser")
    res = soup.select('g-card-section:last-child > div:not([aria-level]) > div > span > span > span')
    return res[0].text if res else None

