from Tables import * 
from stocksChecker import * 

def insert_ticker(chat_id, ticker, needed_price):
    Stocks.set_by_id( (chat_id, ticker) , {Stocks.needed_price : needed_price})

def delete_stocks(chat_id, tickers):
    Stocks.delete().where(Stocks.ticker in tickers and Stocks.chat_id == chat_id).execute()

def get_stocks(chat_id):
    pass

def main():
    Stocks.create_table()
    


if __name__ == "__main__":
    main()
