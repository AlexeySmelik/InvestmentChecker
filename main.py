import requests
import json

res = requests.get('https://bcs-express.ru/webapi2/api/quotes?securCode=GAZP')
print(res.json()['close'])