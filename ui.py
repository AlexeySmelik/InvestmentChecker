import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.tickers = []
    
    def add_ticker(title):
        pass

    def delete_ticker(title):
        pass


class Ticker:
    def __init__(self, price):
        self.price = price


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


token = '1911743302:AAGCO3OdegMhOgONyK-uq8jPqipsZW-PCoA'
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
updater.start_polling()

time.sleep(10)

updater.stop()