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


def request_stocks(update, context):
    update.message.reply_text('Talk to me your securities. Please use this format (Name - Wanted price):\nName1 - 54\nName2 - 17')
    return 2


def get_stocks(update, context):  #TODO
    user = User.get_user(update.effective_chat.id, users)
    for _ in re.findall(r'\w+\-\d+', update.message.text.replace(' ', '')):
        name, cost = _.split('-')
        stock = Stock(name, cost)
        if not stock.is_it_correct():
            update.message.reply_text(f'Mission failed on {stock.name}')
            return 2
        user.try_add_stock(stock)
    update.message.reply_text('Mission complete')
    return ConversationHandler.END


def show_bag(update, context):
    user = User.get_user(update.effective_chat.id, users)
    output = 'Your securities to check:\n'
    for stock in user.stocks:
        output += f'Name: {stock.name} and needed price: {stock.needed_price} \n'
    update.message.reply_text(output)
    return ConversationHandler.END


def show_price(update, context):  #TODO
    return ConversationHandler.END


def request_stock_name(update, context):  #TODO
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
        CommandHandler('check_price', request_stock_name),
        CommandHandler('check_bag', show_bag),
        CommandHandler('add_securities', request_stocks)
    ],
    states={
        1 : [
                MessageHandler(Filters.regex('Add securities'), request_stocks),
                MessageHandler(Filters.regex('Check securitie\'s price'), request_stock_name)
            ],
        2 : [MessageHandler(Filters.text, get_stocks)],
        3 : [MessageHandler(Filters.text, show_price)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)
dp.add_handler(conv_handler)
updater.start_polling()
updater.idle()