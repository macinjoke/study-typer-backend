import yaml
import os

ENV = os.environ.get("ENV")
if ENV == "development":
    config_file = 'config/development.yml'
else:
    config_file = 'config/default.yml'
with open(config_file, 'r') as f:
    config = yaml.load(f)
