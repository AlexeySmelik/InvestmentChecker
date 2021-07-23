from ticker import * 
from tickersChecker import * 

def insert_ticker(id,code,cost):
    if Ticker.get_or_create(id = id, code = code)[1]:
        change_code(code, 1)
    Ticker.set_by_id( (id,code) , {Ticker.cost : cost})


def main():
    pass
    


if __name__ == "__main__":
    main()
