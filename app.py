from flask import Flask
from config import DevelopmentConfig
from apis import api
from core import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api.init_app(app)
db.init_app(app)


if __name__ == '__main__':
    app.run()
