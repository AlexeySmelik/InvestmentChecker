class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.tickers = []
    

    def try_add_tickers(self, ticker):
        is_contain = False
        for t in self.tickers:
            if ticker.shortname == t.shortname:
                t.needed_price = ticker.needed_price
                is_contain = True
                break
        if not is_contain:
            self.tickers.append(ticker) 

    

    def try_delete_ticker(self, ticker):
        for t in self.tickers:
            if ticker.shortname == t.shortname:
                self.tickers.pop(t)
                break




    @staticmethod
    def get_user(chat_id, users):
        for user in users:
            if user.chat_id == chat_id:
                return user
        newUser = User(chat_id)
        users.append(newUser)
        return newUser
            

class Ticker:
    def __init__(self, name, price):
        self.name = name
        self.needed_price = price
        self.shortname = self.name  #TODO


    def is_it_correct(self):
        return True if self.shortname != None else False