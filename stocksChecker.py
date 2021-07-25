from threading import Event, Thread
from Tables import * 
import requests

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def check_tickers(message):
    tickers = Tickers.select()
    for ticker in tickers:
        if (ticker.count == 0):
            ticker.delete_instance()
            continue
        stocks = check_ticker(ticker.name)
        for stock in stocks:
            change_ticker(stock.ticker, -1)
            stock.delete_instance()
        message(stocks)
        
def check_ticker(ticker):
    
    close = requests.get(config.url + ticker).json()['close'].replace(',','.').encode('ascii', 'ignore')

    return Stocks.select().where(Stocks.ticker == ticker and Stocks.needed_price < float(close)).execute()

def change_ticker(name, count):
    ticker = Tickers.get_or_create(name = name)[0]
    new_count = ticker.count + count if ticker.count else count  
    Tickers.set_by_id(name, {'count': new_count})

