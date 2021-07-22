class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.stocks = []
    

    def try_add_stock(self, stock):
        is_contain = False
        for s in self.stocks:
            if stock.ticker == s.ticker:
                s.needed_price = stock.needed_price
                is_contain = True
                break
        if not is_contain:
            self.stocks.append(stock) 
    

    def try_delete_stock(self, stock):
        for s in self.stocks:
            if stock.ticker == s.ticker:
                self.stocks.pop(s)
                break




    @staticmethod
    def get_user(chat_id, users):
        for user in users:
            if user.chat_id == chat_id:
                return user
        newUser = User(chat_id)
        users.append(newUser)
        return newUser
            

class Stock:
    def __init__(self, name, price):
        self.name = name
        self.needed_price = price
        self.ticker = self.name  #TODO


    def is_it_correct(self):
        return True if self.ticker != None else False