class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.tickers = []
    

    def add_tickers(self, tickers):
        self.tickers.append([ticker for ticker in tickers if ticker not in self.tickers])
    

    def delete_ticker(self, ticker):
        self.tickers.pop(ticker)


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


    @staticmethod
    def is_it_correct():
        return True #TODO