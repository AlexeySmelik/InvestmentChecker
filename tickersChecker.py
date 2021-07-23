from threading import Event, Thread
from ticker import * 
import requests

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def check_tickers():
    codes = Code.select(Code.code)
    for code in codes:
        tickers = check_code(code.code)
        change_code(code.code, -tickers.cursor.rowcount)
        for ticker in tickers:
            ticker.delete_instance()
        
def check_code(code):

    close= requests.get(config.url + code).json()['close'].replace(',','.')

    return Ticker.select().where(Ticker.code == code and Ticker.cost < close).execute()

def change_code(code, count):
    secure = Code.get_or_create(code = code)[0]
    temp = secure.count + count if secure.count else count  
    Code.set_by_id(code, {'count': temp})

