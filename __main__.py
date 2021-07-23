import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from modules import *   
import tickersChecker

def start(update, context):
    User.get_user(update.effective_chat.id, users)
    reply_keyboard = [['Add securities', 'Check bag', 'Remove securities']]
    update.message.reply_text(
        'I\'m a bot, I can check securitie\'s price and tell you when the security will cost as much as you need)0))',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 1


def request_stocks_to_add(update, context):
    update.message.reply_text('Talk to me your securities. Please use this format (Name - Wanted price):\nName1 - 54\nName2 - 17')
    return 2


def get_stocks_to_add(update, context):  #TODO
    user = User.get_user(update.effective_chat.id, users)
    for _ in re.findall(r'\w+\-\d+', update.message.text.replace(' ', '')):
        name, cost = _.split('-')
        stock = Stock(name, cost)
        if not user.try_add_stock(stock):
            update.message.reply_text(f'Mission failed on {stock.name}. Try again')
            return 2
    update.message.reply_text('Mission complete')
    return ConversationHandler.END


def request_stocks_to_remove(update, context):
    update.message.reply_text('Talk to me your securities to remove. Please use this format (Name):\nName1\nName2')
    return 3


def get_stocks_to_remove(update, context):  #TODO
    user = User.get_user(update.effective_chat.id, users)
    for _ in re.findall(r'\w+', update.message.text.replace(' ', '')):
        if not user.try_delete_stock(Stock(_)):
            update.message.reply_text(f'Mission failed on {_}. No such stocks in your bag. Try again')
            return 3
    update.message.reply_text('Mission complete')
    return ConversationHandler.END


def show_bag(update, context):
    user = User.get_user(update.effective_chat.id, users)
    output = 'Your securities to check:\n' if user.stocks else 'Empty'
    for stock in user.stocks:
        output += f'Name: {stock.name} and needed price: {stock.needed_price}\n'
    update.message.reply_text(output)
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('I hope we can talk again some day.')
    return ConversationHandler.END


def send_messages(tickers):
    for ticker in tickers:
        updater.bot.send_message(chat_id=ticker.id, text=f'Check {ticker.code}')


users = []

token = '1911743302:AAGCO3OdegMhOgONyK-uq8jPqipsZW-PCoA'
updater = Updater(token=token, use_context=True)
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
updater.start_polling()
updater.idle()

tickersChecker.call_repeatedly(5 ,tickersChecker.check_tickers) #SetInterval
