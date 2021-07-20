import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from moduls import *    


def start(update, context):
    User.get_user(update.effective_chat.id, users)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I can check securities and tell you when the security will cost as much as you need!")
    

def wait_tickers(update, context):
    user = User.get_user(update.effective_chat.id, users)
    user.user_script.execute(lambda s : context.bot.send_message(chat_id=update.effective_chat.id, text=s))


def get_tickers(update, context):
    user = User.get_user(update.effective_chat.id, users)
    user.user_script.execute(lambda s : context.bot.send_message(chat_id=update.effective_chat.id, text=s), update.message.text)


token = '1911743302:AAGCO3OdegMhOgONyK-uq8jPqipsZW-PCoA'
users = []
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('specify_securities', wait_tickers))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), get_tickers))
updater.start_polling()

updater.idle()
print(users)