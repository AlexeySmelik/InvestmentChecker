from enum import Enum

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.user_script = UserScript(self)
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


class StateScript(Enum):
    WaitTickers = 0
    GetTickers = 1
    GetNeededPrices = 2


class UserScript:
    def __init__(self, user):
        self.state = StateScript.WaitTickers
        self.user = user

    def execute(self, action = None, title = ''):
        if self.state == StateScript.WaitTickers:
            action("Please talk to me your securities (like 'Apple, Google' and etc.)!")
            self.state = StateScript.GetTickers
        elif self.state == StateScript.GetTickers:
            tickers = Ticker.parse_string(title)
            self.user.add_tickers(tickers)
            action("Okay")
            self.state = StateScript.WaitTickers
            

class Ticker:
    def __init__(self, name, price):
        self.name = name
        self.needed_price = price
    

    @staticmethod
    def parse_string(title):
        tickers = [_ for _ in title.replace(',', ' ').split(' ') if _ and Ticker.is_it_correct(_)]
        return tickers

    @staticmethod
    def is_it_correct():
        return True #TODO