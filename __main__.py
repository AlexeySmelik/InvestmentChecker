import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from modules import *    


def start(update, context):
    User.get_user(update.effective_chat.id, users)
    reply_keyboard = [['Add securities', 'Check securities', 'Remove securities']]
    update.message.reply_text(
        'I\'m a bot, I can check securitie\'s price and tell you when the security will cost as much as you need)0))',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 1


def request_tickers(update, context):
    update.message.reply_text(
        '''Talk to me your securities. Please use this format (Name - Wanted price):
                Name1 - 54
                Name2 - 17
        '''
    )
    return 2


def get_tickers(update, context):  #TODO
    user = User.get_user(update.effective_chat.id, users)
    for _ in re.findall(r'\w+\-\d+', update.message.text.replace(' ', '')):
        name, cost = _.split('-')
        ticker = Ticker(name, cost)
        if not ticker.is_it_correct():
            update.message.reply_text(f'Mission failed on {ticker.name}')
            return 2
        user.try_add_tickers(ticker)
    update.message.reply_text('Mission complete')
    return ConversationHandler.END


def show_bag(update, context):
    user = User.get_user(update.effective_chat.id, users)
    output = 'Your securities to check:\n'
    for ticker in user.tickers:
        output += f'Name: {ticker.name} and needed price: {ticker.needed_price} \n'
    update.message.reply_text(output)
    return ConversationHandler.END


def show_price(update, context):  #TODO
    return ConversationHandler.END


def request_ticker(update, context):  #TODO
    return 3


def cancel(update, context):
    update.message.reply_text('I hope we can talk again some day.')
    return ConversationHandler.END


users = []

token = '1911743302:AAGCO3OdegMhOgONyK-uq8jPqipsZW-PCoA'
updater = Updater(token=token, use_context=True)
dp = updater.dispatcher
conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CommandHandler('check_price', request_ticker),
        CommandHandler('check_bag', show_bag),
        CommandHandler('add_securities', request_tickers)
    ],
    states={
        1 : [
                MessageHandler(Filters.regex('Add securities'), request_tickers),
                MessageHandler(Filters.regex('Check securitie\'s price'), request_ticker)
            ],
        2 : [MessageHandler(Filters.text, get_tickers)],
        3 : [MessageHandler(Filters.text, show_price)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)
dp.add_handler(conv_handler)
updater.start_polling()
updater.idle()