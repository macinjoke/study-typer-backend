import redis
import re

rds = redis.StrictRedis(decode_responses=True)

IDEAL_MAX_WORD_COUNT = 25


def main():
    word_keys = rds.keys('word:*')
    for word_key in word_keys:
        ja = rds.hget(word_key, 'ja')
        short_ja = convert_ja_short(ja)
        result = rds.hset(word_key, 'ja', short_ja)
        print(result)


def convert_ja_short(ja):
    sentences = ja.split('/')
    converted_sentences = [
        convert_sentence(sentence) for sentence in sentences
    ]
    result_sentences = select_sentences(converted_sentences)
    return '\n'.join(result_sentences)


def convert_sentence(sentence):
    # セミ句を1つのみ残す
    output = sentence.split(';')[0]

    # カンマ句を2つ以下にする
    # `()`の中に `,` が含まれている場合は何もしない
    if not re.search(r'\([^)]*,[^)]*\)', output):
        output = ', '.join(output.split(',')[:2])

    # 7文字以上含まれる`()`を取り除く
    output = re.sub(r'\([^)]{7,}?\)', '', output)

    # `《米》`, `《英》` を `[米]`, `[英]` に変える
    output = re.sub(r'《([米|英]).*?》', r'[\1]', output)

    # `〈U〉`, `〈C〉` の囲いを変える
    output = re.sub(r'〈([U|C])〉', r'<\1>', output)

    # `…‘を'` を `(…を)` に置き換える。( `‘に'` なども同様)
    output = re.sub(r'…‘(.+?)\'', r'(…\1)', output)
    # `‘を'` を `を` に置き換える。( `‘に'` なども同様)
    output = re.sub(r'‘(.+?)\'', r'\1', output)

    return output


def select_sentences(sentences):
    if len(sentences) <= 2:
        return sentences
    first = sentences[0]
    initial_index = int(len(sentences) * 0.7)
    index = initial_index

    # 2つめの候補としてIDEAL_MAX_WORD_COUNT 文字以下の文を探す。
    # 最初は7割より上のindex を探し、なかった場合は7割より下のindexを探す。
    # それでもなかった場合は initial_indexを選択する
    # (その場合IDEAL_MAX_WORD_COUNT文字以上になってしまう)
    while True:
        if len(sentences) == index:
            index = initial_index
            while True:
                if index == 0:
                    index = initial_index
                    break
                if len(sentences[index]) > IDEAL_MAX_WORD_COUNT:
                    index -= 1
                else:
                    break
            break
        if len(sentences[index]) > IDEAL_MAX_WORD_COUNT:
            index += 1
        else:
            break
    second = sentences[index]
    return [first, second]


if __name__ == '__main__':
    main()
