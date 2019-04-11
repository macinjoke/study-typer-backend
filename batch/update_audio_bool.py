"""
audioディレクトリに入っている `.flac` ファイルからファイル名を取り出し、
redisに存在するwordならaduio フラグをtrue にして audio_available リストに追加する。
すでにaudio_available な単語はスルーする。
ファイル名とredisに英単語名のハイフンやアンスコの有無などの差異は吸収して同一のものとする。
あれ？ここで差異吸収したらフロント側で、 `redisの英単語名.flac` を再生しようとしたときに
再生できなくなるな...。
TODO: 再吸収したらファイル名の方を変更する。
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
        word = get_existing_word(en)
        if word is not None:
            for i in range(1, 31):
                if rds.zscore(f'words:{i}', word) is not None:
                    count += 1
                    print(f'{i}: {word} のaudioを有効化します。')
                    set_audio(word, i)


def get_existing_word(en):
    """
    ハイフン-やアンスコ_などを含むファイル名を、redisのword:{hoge} のkeyに存在する
    英単語に直して返す。redisに存在しなければNone を返す。
    :param en: 英単語の文字列 
    :return: redisのキーに存在する英単語文字列 or None
    """
    en = en.lower()
    if rds.exists(f'word:{en}'):
        return en
    elif en.find('-') != -1:
        replaced = en.replace("-", " ")
        if rds.exists(f'word:{replaced}'):
            return replaced
    elif en.find('_') != -1:
        replaced = en.replace("_", " ")
        if rds.exists(f'word:{replaced}'):
            return replaced
        replaced = en.replace("_", "-")
        if rds.exists(f'word:{replaced}'):
            return replaced
    else:
        return None


def set_audio(word, rank):
    rds.hset(f'word:{word}', 'audio', 'true')
    rds.zrem(f'words:{rank}', word)
    rds.zadd(f'words:{rank}:audio_available', int(time.time()), word)


if __name__ == '__main__':
    main()

