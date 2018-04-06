from flask import Flask, request, abort
from flask_cors import CORS
import redis
import json
import random
from study_typer.config import config

app = Flask(__name__)
CORS(app)

rds = redis.StrictRedis(
    decode_responses=True,
    host=config['redis']['host'],
    port=config['redis']['port']
)
WORDS_COUNT = 10


@app.route("/api/words", methods=['GET'])
def index():
    try:
        rds.ping()
    except redis.exceptions.ConnectionError:
        return abort(503)
    rank = request.args.get('rank', 0)
    key = 'words:{}:audio_available'.format(rank)
    word_ids = rds.zrange(key, 0, -1)
    if len(word_ids) > 10:
        word_ids = random.sample(word_ids, k=WORDS_COUNT)

    words = []
    for word_id in word_ids:
        key = 'word:{}'.format(word_id)
        result = rds.hgetall(key)
        word = {
            'en': word_id,
            'ja': result['ja'],
            'rank': result['rank']
        }
        words.append(word)
    return json.dumps(words)
