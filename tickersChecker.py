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

def check_tickers(message):
    print(1)
    codes = Code.select()
    for code in codes:
        if (code.count == 0):
            print("kill "+ code.code)
            code.delete_instance()
            continue
        tickers = check_code(code.code)
        for ticker in tickers:
            change_code(ticker.code, -1)
            ticker.delete_instance()
        message(tickers)
        
def check_code(code):

    close= requests.get(config.url + code).json()['close'].replace(',','.')

    return Ticker.select().where(Ticker.code == code and Ticker.cost < close).execute()

def change_code(code, count):
    secure = Code.get_or_create(code = code)[0]
    temp = secure.count + count if secure.count else count  
    Code.set_by_id(code, {'count': temp})

