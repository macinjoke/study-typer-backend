"""
現在redisにあるデータをランク別、音声ありなし別でわかりやすく表示する
"""

import redis

rds = redis.StrictRedis(decode_responses=True)


def show_all():
    print(f'key counts: {rds.dbsize()}')
    for i in range(30):
        show_word_count(i)


def show_word_count(i):
    no_audio = rds.zrange(f'words:{i}', 0, -1)
    audio = rds.zrange(f'words:{i}:audio_available', 0, -1)
    print(f'{i:2}: no_audio {len(no_audio):5}, audio {len(audio):5}')



if __name__ == '__main__':
    show_all()