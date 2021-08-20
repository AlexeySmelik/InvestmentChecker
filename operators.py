import operator
import peewee as pw
import strings as s
import config, re
from meta import Singleton
from checkers import StockChecker
from playhouse.mysql_ext import MySQLConnectorDatabase
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup


class BaseModel(pw.Model):
    class Meta:
        database = MySQLConnectorDatabase(
            host = config.db_host,
            user = config.db_user,
            password = config.db_password,
            database = config.db_name,
        )


class Stocks(BaseModel):
    chat_id = pw.IntegerField(column_name='chat_id')
    ticker = pw.CharField(max_length= 10, column_name='ticker')
    needed_price = pw.FloatField(column_name='needed_price')

    class Meta:
        primary_key = pw.CompositeKey('chat_id', 'ticker')
        table_name = 'Stocks'


class DBoperator(metaclass=Singleton):
    __table = Stocks
    __checker: StockChecker = None


    def __init__(self) -> None:
        self.__checker = StockChecker()
        self.__table.create_table()
    
    
    def get_user_stocks(self, chat_id):
        return (self.__table
                    .select(self.__table.ticker, self.__table.needed_price)
                    .where(self.__table.chat_id == chat_id)
                    .execute())

    
    def try_add_stock(self, chat_id, name, needed_price):
        ticker = self.__checker.get_ticker(name)
        if not ticker:
            return False
        self.__table.get_or_create(chat_id = chat_id, ticker = ticker)
        self.__table.set_by_id((chat_id, ticker), {self.__table.needed_price : needed_price})
        return True

    
    def delete_user_stocks(self, chat_id, names):
        correct_tickers = list(filter(None, map(lambda name: self.__checker.get_ticker(name), names)))
        for ticker in correct_tickers:
            (self.__table
                .delete()
                .where(self.__table.chat_id == chat_id, self.__table.ticker == ticker)
                .execute())


    def check_tickers(self, message):    
        tickers = self.__table.select(self.__table.ticker).distinct()
        for ticker in tickers:  # chunked !! api model
            stocks = self.pop_stocks(ticker.ticker)
            message(stocks)
        

    def pop_stocks(self, ticker):
        close = self.__checker.get_cost(ticker).replace(',','.').encode('ascii', 'ignore')
        stocks = (self.__table
                        .select()
                        .where(self.__table.ticker == ticker and self.__table.needed_price < float(close))
                        .execute())
        (self.__table
                .delete()
                .where(self.__table.ticker == ticker and self.__table.needed_price < float(close))
                .execute())
        return stocks


class TGoperator(metaclass=Singleton):
    __updater: Updater = None
    __db_oper: DBoperator = None


    def __init__(self, token, db_oper):
        self.__updater = Updater(token=token, use_context=True)
        self.__db_oper = db_oper 


    def start_bot(self):
        self.__updater.start_polling()
        self.__updater.idle()


    def __start(self, update, context):
        reply_keyboard = [['Add securities', 'Check bag', 'Remove securities']]
        update.message.reply_text(
            s.start_message,
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 1
    

    def __get_stocks_to_add(self, update, context):
        chat_id = update.effective_chat.id
        for _ in re.findall(r'\w+\-\d+', update.message.text.replace(' ', '')):
            name, needed_price = _.split('-')
            if not self.__db_oper.try_add_stock(chat_id, name, needed_price):
                update.message.reply_text(f'Mission failed on {name}. Try again')
                return 2
            update.message.reply_text(f'Mission complete on {name}')
        return ConversationHandler.END


    def __request_stocks_to_add(self, update, context):
        update.message.reply_text(s.request_to_add_message)
        return 2


    def __request_stocks_to_remove(self, update, context):
        update.message.reply_text(s.request_to_del_message)
        return 3

    
    def __get_stocks_to_remove(self, update, context):
        chat_id = update.effective_chat.id
        self.__db_oper.delete_user_stocks(chat_id, re.findall(r'\w+', update.message.text.replace(' ', '')))
        update.message.reply_text('Mission complete')
        return ConversationHandler.END


    def __show_bag(self, update, context):
        chat_id = update.effective_chat.id
        user_stocks = self.__db_oper.get_user_stocks(chat_id)
        output = 'Your securities to check:\n' if user_stocks else 'Empty'
        for stock in user_stocks:
            output += f'Ticker: {stock.ticker} and needed price: {stock.needed_price}\n'
        update.message.reply_text(output)
        return ConversationHandler.END


    def __cancel(self, update, context):
        update.message.reply_text(s.cancel_message)
        return ConversationHandler.END

    
    def send_messages(self, stocks):
        for stock in stocks:
            self.__updater.bot.send_message(chat_id= stock.chat_id, text=f'Check {stock.ticker}')

    
    def set_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', self.__start),
                CommandHandler('check_bag', self.__show_bag),
                CommandHandler('add_securities', self.__request_stocks_to_add),
                CommandHandler('del_securities', self.__request_stocks_to_remove)
            ],
            states={
                1 : [
                        MessageHandler(Filters.regex('Add securities'), self.__request_stocks_to_add),
                        MessageHandler(Filters.regex('Check bag'), self.__show_bag),
                        MessageHandler(Filters.regex('Remove securities'), self.__request_stocks_to_remove)
                    ],
                2 : [MessageHandler(Filters.text, self.__get_stocks_to_add)],
                3 : [MessageHandler(Filters.text, self.__get_stocks_to_remove)],
            },
            fallbacks=[CommandHandler('cancel', self.__cancel)],
            allow_reentry=True
        )
        self.__updater.dispatcher.add_handler(conv_handler)
