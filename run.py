from typing_app.flask_main import app
from typing_app.config import config

if __name__ == '__main__':
    app.run(
        host=config['app']['host'], port=config['app']['port'],
        debug=config['app']['debug']
    )
