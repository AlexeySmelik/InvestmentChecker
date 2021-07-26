import stocksChecker, re, config
import strings as s
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from modules import *   


def start(update, context):
    reply_keyboard = [['Add securities', 'Check bag', 'Remove securities']]
    update.message.reply_text(s.start_message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return 1


def request_stocks_to_add(update, context):
    update.message.reply_text(s.request_to_add_message)
    return 2


def get_stocks_to_add(update, context):
    user = User(update.effective_chat.id)
    for _ in re.findall(r'\w+\-\d+', update.message.text.replace(' ', '')):
        name, cost = _.split('-')
        stock = Stock(name, cost)
        if not user.try_add_stock(stock):
            update.message.reply_text(f'Mission failed on {stock.name}. Try again')
            return 2
        update.message.reply_text(f'Mission complete on {stock.name} : ticker: {stock.ticker}')
    return ConversationHandler.END


def request_stocks_to_remove(update, context):
    update.message.reply_text(s.request_to_del_message)
    return 3


def get_stocks_to_remove(update, context):
    user = User(update.effective_chat.id)
    user.delete_user_stocks(re.findall(r'\w+', update.message.text.replace(' ', '')))
    update.message.reply_text('GG!')
    return ConversationHandler.END


def show_bag(update, context):
    """user = User(update.effective_chat.id)
    output = 'Your securities to check:\n' if user.stocks else 'Empty'
    for stock in user.stocks:
        output += f'Name: {stock.name} and needed price: {stock.needed_price}\n'
    update.message.reply_text(output)"""
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text(s.cancel_message)
    return ConversationHandler.END


def send_messages(stocks):
    for stock in stocks:
        updater.bot.send_message(chat_id= stock.chat_id, text=f'Check {stock.ticker}')


updater = Updater(token=config.token, use_context=True)
dp = updater.dispatcher
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CommandHandler('check_bag', show_bag),
        CommandHandler('add_securities', request_stocks_to_add),
        CommandHandler('del_securities', request_stocks_to_remove)
    ],
    states={
        1 : [
                MessageHandler(Filters.regex('Add securities'), request_stocks_to_add),
                MessageHandler(Filters.regex('Check bag'), show_bag),
                MessageHandler(Filters.regex('Remove securities'), request_stocks_to_remove)
            ],
        2 : [MessageHandler(Filters.text, get_stocks_to_add)],
        3 : [MessageHandler(Filters.text, get_stocks_to_remove)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)
dp.add_handler(conv_handler)

stocksChecker.call_repeatedly(config.interval, stocksChecker.check_tickers, send_messages) #SetInterval

updater.start_polling()
updater.idle()

