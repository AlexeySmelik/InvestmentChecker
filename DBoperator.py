from Tables import * 
from stocksChecker import * 


def insert_ticker(chat_id, ticker, needed_price):
    Stocks.get_or_create(chat_id = chat_id, ticker = ticker)
    Stocks.set_by_id((chat_id, ticker), {Stocks.needed_price : needed_price})


def delete_stocks(chat_id, tickers):
    for ticker in tickers:
        _ = Stocks.get_or_none(Stocks.chat_id == chat_id, Stocks.ticker == ticker)
        if _:
            _.delete_instance()


def get_stocks(chat_id):
    return Stocks.select(Stocks.ticker, Stocks.needed_price).where(Stocks.chat_id == chat_id).execute()


def main():
    Stocks.create_table()


if __name__ == "__main__":
    main()