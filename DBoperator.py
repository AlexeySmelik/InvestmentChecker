from Stocks import * 
from stocksChecker import * 

def insert_ticker(chat_id, ticker, needed_price):
    if Stocks.get_or_create(chat_id = chat_id, ticker = ticker)[1]:
        change_ticker(ticker, 1)
    Stocks.set_by_id( (chat_id, ticker) , {Stocks.needed_price : needed_price})

def delete_stocks(chat_id, stocks):
    pass

def get_stocks(chat_id):
    pass

def main():
    Stocks.create_table()
    Tickers.create_table()
    


if __name__ == "__main__":
    main()
