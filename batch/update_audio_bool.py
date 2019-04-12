"""
audioディレクトリに入っている `.flac` ファイルからファイル名を取り出し、
redisに存在するwordならaduio フラグをtrue にして audio_available リストに追加する。
すでにaudio_available な単語はスルーする。
"""
import redis
import subprocess
import time

rds = redis.StrictRedis(decode_responses=True)


def main():
    result = subprocess.run(
        ["ls", "-1", "/Users/makinoshunni/.ghq/github.com/macinjoke/study-typer-frontend/dist/assets/audio"],
        stdout=subprocess.PIPE
    )
    filenames = result.stdout.decode('utf-8').split('\n')
    en_words = [
        filename[:filename.rfind('.flac')] for filename in filenames
        if filename.rfind('.flac') != -1
    ]
    print(f'{len(en_words)} 個の単語についてredisを探索します')
    count = 0
    for en in en_words:
        for i in range(1, 31):
            if rds.zscore(f'words:{i}', en) is not None:
                count += 1
                print(f'{i}: {en} のaudioを有効化します。')
                set_audio(en, i)


# def get_existing_word(en):
#     """
#     ハイフン-やアンスコ_などを含むファイル名を、redisのword:{hoge} のkeyに存在する
#     英単語に直して返す。redisに存在しなければNone を返す。
#     :param en: 英単語の文字列
#     :return: redisのキーに存在する英単語文字列 or None
#     """
#     en = en.lower()
#     if rds.exists(f'word:{en}'):
#         return en
#     elif en.find('-') != -1:
#         replaced = en.replace("-", " ")
#         if rds.exists(f'word:{replaced}'):
#             return replaced
#     elif en.find('_') != -1:
#         replaced = en.replace("_", " ")
#         if rds.exists(f'word:{replaced}'):
#             return replaced
#         replaced = en.replace("_", "-")
#         if rds.exists(f'word:{replaced}'):
#             return replaced
#     else:
#         return None


def set_audio(word, rank):
    rds.hset(f'word:{word}', 'audio', 'true')
    rds.zrem(f'words:{rank}', word)
    rds.zadd(f'words:{rank}:audio_available', int(time.time()), word)


if __name__ == '__main__':
    main()

