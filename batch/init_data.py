
import json
import redis
import re
import time

EJDIC_PATTERN = r'([a-z][a-z\- ]{2,})([^,a-zA-Z].*)'
rds = redis.StrictRedis(decode_responses=True)


def input_from_words_json():
    with open('words.json', 'r') as f:
        words = json.load(f)['words']
    rds.delete('words')
    rds.rpush('words', *words)
    words = rds.lrange('words', 0, -1)
    print(words)


def init_from_ejdic():
    with open('_my_gitignored/ejdic-hand-utf8.txt', 'r') as f:
        lines = f.readlines()
    words = []
    for line in lines:
        m = re.match(EJDIC_PATTERN, line)
        if m:
            print(m)
            print('1: {} | 2: {}'.format(m.group(1), m.group(2)))
            words.append({
                'en': m.group(1),
                'ja': m.group(2).replace('\t', '').replace(' ', '')
            })
        else:
            print('not match', line)
    print(len(lines))
    rds.flushdb()
    for word in words:
        add_word(**word)


def add_word(en, ja, rank=0):
    key = 'words:{}'.format(rank)
    rds.zadd(key, int(time.time()), en)
    key = 'word:{}'.format(en)
    rds.hmset(key, {'ja': ja, 'rank': rank})


if __name__ == '__main__':
    # input_from_words_json()
    init_from_ejdic()
