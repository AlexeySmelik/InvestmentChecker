from threading import Event, Thread
from operators import DBoperator, TGoperator
import config


def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set


db_oper = DBoperator()
tg_oper = TGoperator(config.token, db_oper)
tg_oper.set_handlers()
call_repeatedly(config.interval, db_oper.check_tickers, tg_oper.send_messages) #SetInterval
tg_oper.start_bot()