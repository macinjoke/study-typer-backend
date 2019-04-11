"""
Google 検索の英単語のヒット数を取得する
"""
from bs4 import BeautifulSoup
import requests
import os.path
import re

ENDPOINT = 'https://google.com'
PATH = 'search'
URL = os.path.join(ENDPOINT, PATH)
# not match less hit num because '約' is not attached.
HIT_NUM_PATTERN_JA = r'約 ([\d,]*) 件'
HIT_NUM_PATTERN_EN = r'About ([\d,]*) results'


def fetch_google_hit_count(search_word):
    payload = {'q': search_word}
    r = requests.get(URL, params=payload)
    print(r.url)
    bs = BeautifulSoup(r.text, 'html.parser')
    div = bs.find('div', attrs={'id': 'resultStats'})
    print(div)
    m = re.match(HIT_NUM_PATTERN_JA, div.string)
    if not m:
        m = re.match(HIT_NUM_PATTERN_EN, div.string)
    if m:
        hit_count_str = m.group(1)
        hit_count = int(hit_count_str.replace(',', ''))
        return hit_count
    else:
        print('not match')


if __name__ == '__main__':
    hit_count = fetch_google_hit_count('ask')
    print(hit_count)
