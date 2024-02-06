import logging
from logging.handlers import RotatingFileHandler
import os

from flask import  Flask
from config import Config

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.debug=False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "login"


if not os.path.exists("logs"):
    os.mkdir("logs")
    handler = RotatingFileHandler("logs/mblog.log", maxBytes=10240,backupCount=10)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    handler.setLevel(logging.INFO)

    app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('mblog startup')

from app import routes, models, errors
