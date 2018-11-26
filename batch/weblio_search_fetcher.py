from bs4 import BeautifulSoup
import requests
import os.path
import re

ENDPOINT = 'http://ejje.weblio.jp'
PATH = 'content'
RANK_PATTERN = r'\s*(\d\d?)\s*'


def fetch_weblio_rank(search_word):
    url = os.path.join(ENDPOINT, PATH, search_word)
    print(url)

    try:
        r = requests.get(url)
    except (ConnectionError, requests.ConnectionError):
        print('ConnectionError')
        return 'ConnectionError'
    except requests.ReadTimeout:
        print('ReadTimeout')
        return 'ReadTimeout'

    bs = BeautifulSoup(r.text, 'html.parser')
    div = bs.find('span', attrs={'class': 'learning-level-content'})
    if div is None:
        print('specified word was not found')
        return 'not_found'
    print(div)
    m = re.match(RANK_PATTERN, div.string)
    if m:
        rank = int(m.group(1))
        return rank
    else:
        print('not match')

if __name__ == '__main__':
    rank = fetch_weblio_rank('kofdsa dfakos fksdao')
    print(rank)
