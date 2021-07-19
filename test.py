import pandas as pd
import yfinance as yf

tickers = 'YNDX.ME GAZP.ME LSRG.ME'
data = yf.download(tickers, period='1d', interval='1m', group_by='ticker')