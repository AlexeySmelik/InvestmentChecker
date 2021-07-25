import requests
from bs4 import BeautifulSoup as BS
import config

name = 'YANDEX'
url = f"https://google.com/search?q={name}+акция"
headers = {"user-agent" : config.user_agent}
resp = requests.get(url, headers=headers)
start_index = resp.text[resp.text.index('MCX:'):].index('"') + resp.text.index('MCX:')
end_index = resp.text[start_index:].index('"') + start_index
print(start_index, end_index)
soup = BS(resp.content, "html.parser")
result = soup.find('span', {'class' : resp.text[start_index:end_index]})
print(result.text, resp.text[start_index:end_index])