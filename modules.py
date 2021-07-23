from DBoperator import insert_ticker

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.stocks = []
    

    def try_add_stock(self, stock):
        if not stock.is_it_correct():
            return False
        insert_ticker(self.chat_id, stock.ticker, stock.needed_price)

        is_contain = False
        for s in self.stocks:
            if stock.ticker == s.ticker:
                s.needed_price = stock.needed_price
                is_contain = True
                break

        if not is_contain:
            stock.try_add_user(self)
            self.stocks.append(stock)
        return True
    

    def try_delete_stock(self, stock):
        for s in self.stocks:
            if stock.ticker == s.ticker:
                self.stocks.remove(s)
                return True
        return False


    @staticmethod
    def get_user(chat_id, users):
        for user in users:
            if user.chat_id == chat_id:
                return user
        newUser = User(chat_id)
        users.append(newUser)
        return newUser
            

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
        self.ticker = self.test[self.name]  #TODO
        self.users = []


    def try_add_user(self, user):
        
        for u in self.users:
            if user.chat_id == u.chat_id:
                return False
        print(self.needed_price)
        self.users.append(user)
        return True


    def is_it_correct(self):
        return True if self.ticker != None else False