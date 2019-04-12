"""
Rank を 取得し、redis にrank データを付与する。
"""
import redis
import random
import time
from weblio_search_fetcher import fetch_weblio_rank

rds = redis.StrictRedis(decode_responses=True)

ACCESS_INTERVAL = 1
WORDS_AMOUNT = 1000


def main():
    print('access interval: {}, words amount: {}'
          .format(ACCESS_INTERVAL, WORDS_AMOUNT))
    print(f'keys count: {rds.dbsize()}')
    unranked_words = rds.zrange('words:0', 0, -1)
    word_ids_sample = random.sample(unranked_words, k=WORDS_AMOUNT)
    for i, word in enumerate(word_ids_sample):
        time.sleep(ACCESS_INTERVAL)
        print(i)
        rank = fetch_weblio_rank(word)
        if rank is None:
            continue
        rds.hset('word:{}'.format(word), 'rank', rank)
        rds.zrem('words:0', word)
        rds.zadd('words:{}'.format(rank), int(time.time()), word)
        print('Rank of `{}` is {}'.format(word, rank))
    print(f'keys count: {rds.dbsize()}')


if __name__ == '__main__':
    main()
