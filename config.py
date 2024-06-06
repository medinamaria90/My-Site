from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, request
from flask_mail import Mail
from dotenv import load_dotenv
from email.mime.text import MIMEText
from flask_migrate import Migrate
from flask import g
import os
import datetime

load_dotenv()


class Config:
    def __init__(self, production):
        self.production = production

    def set_secret_key(self):
        return {
            'SECRET_KEY': os.getenv('FLASK_SECRET_KEY'),
        }

    def create_db_alchemy(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        db = SQLAlchemy(app)
        migrate = Migrate(app, db)
        return db

    def debug(self):
        return {
            "DEBUG": not self.production
        }


# App creation and config
app = Flask(__name__)
if os.getenv('PRODUCTION') == "False":
    production = False
else:
    production = True
if production == False:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
config = Config(production=production)

db = config.create_db_alchemy(app)
app.config.update(config.set_secret_key())
app.config.update(config.debug())

now = datetime.datetime.now()
current_date = now.today().date()
current_year = now.year
