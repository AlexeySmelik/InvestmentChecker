from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from modules import *    


def start(update, context):
    User.get_user(update.effective_chat.id, users)
    reply_keyboard = [['Specify securities', 'Check securities']]
    update.message.reply_text(
        'I\'m a bot, I can check securitie\'s price and tell you when the security will cost as much as you need)0))',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return 1


def request_tickers(update, context):
    User.get_user(update.effective_chat.id, users)
    update.message.reply_text(
        '''Talk to me your securities. Please use this format (Name - Wanted price):
                Name1 - 54
                Name2 - 17
        '''
    )
    return 2


def get_tickers(update, context):  #TODO
    user = User.get_user(update.effective_chat.id, users)
    arr = list(filter(lambda s: s != ' ' or s != '-' or s != '\n', update.message.text))
    tickers = [Ticker(arr[i], arr[i + 1]) for i in range(0, len(arr) - 1, 2)]
    user.add_tickers(tickers)
    update.message.reply_text('Mission complete!')
    return ConversationHandler.END


def check_price(update, context):  #TODO
    pass


def request_ticker(update, context):  #TODO
    pass


def cancel(update, context):
    update.message.reply_text('I hope we can talk again some day.')
    return ConversationHandler.END


token = '1911743302:AAGCO3OdegMhOgONyK-uq8jPqipsZW-PCoA'
users = []
updater = Updater(token=token, use_context=True)
dp = updater.dispatcher
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1 : [
                MessageHandler(Filters.regex('Specify securities'), request_tickers),
                MessageHandler(Filters.regex('Check securitie\'s price'), request_ticker)
            ],
        2 : [MessageHandler(Filters.text, get_tickers)],
        3 : [MessageHandler(Filters.text, check_price)]
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)
dp.add_handler(conv_handler)
updater.start_polling()
updater.idle()