import yaml
import os
import redis

ENV = os.environ.get("ENV")
if ENV == "development":
    config_file = 'config/development.yml'
else:
    config_file = 'config/default.yml'
with open(config_file, 'r') as f:
    config = yaml.load(f)

redis_url = os.getenv("REDIS_URL")
if redis_url:
    rds = redis.StrictRedis.from_url(redis_url, decode_responses=True)
else:
    rds = redis.StrictRedis(
        decode_responses=True,
        host=config['redis']['host'],
        port=config['redis']['port'],
    )


