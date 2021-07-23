from DBoperator import insert_ticker, get_stocks, delete_stocks

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
    test = {
        'YANDEX':'YNDX',
        'YNDX': 'YNDX',
        'GAZPROM': 'GAZP',
        'GAZP' : 'GAZP'
    }


    def __init__(self, name, price = 54):
        self.name = name.upper()
        self.needed_price = price
        self.ticker = self.test[self.name]


    def is_it_correct(self):
        return self.ticker