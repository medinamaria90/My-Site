from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

production = False


class Config:

    def __init__(self, production = False):
        self.production = production
        if production == False:
            self.MYSQL_HOST = os.getenv('MYSQL_LOCAL_HOST')
            self.MYSQL_USER = os.getenv('MYSQL_LOCAL_USER')
            self.MYSQL_PASSWORD = os.getenv('MYSQL_LOCAL_PASSWORD')
            self.MYSQL_DB = os.getenv('MYSQL_LOCAL_DB')
        elif production == True:
            self.MYSQL_HOST = os.getenv('MYSQL_HOST')
            self.MYSQL_USER = os.getenv('MYSQL_USER')
            self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
            self.MYSQL_DB = os.getenv('MYSQL_DB')

    def set_secret_key(self):
        return {
            'SECRET_KEY' : os.getenv('FLASK_SECRET_KEY'),
        }

    def create_db_alchemy(self, app):
        app.config["SQLALCHEMY_DATABASE_URI"] = self.get_db_uri()
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy(app)
        return db

    def get_db_uri(self):
        db_config = self.app_sql_db()
        db_uri = f"mysql://{db_config['MYSQL_USER']}:{db_config['MYSQL_PASSWORD']}@{db_config['MYSQL_HOST']}/{db_config['MYSQL_DB']}"
        return db_uri

    def app_sql_db(self):
        return {
            'MYSQL_HOST': self.MYSQL_HOST,
            'MYSQL_USER': self.MYSQL_USER,
            'MYSQL_PASSWORD': self.MYSQL_PASSWORD,
            'MYSQL_DB': self.MYSQL_DB,
        }

    def debug(self):
        if self.production == False:
            return {
                "DEBUG" : True
            }
        else:
            return {
                "DEBUG": False
            }

    def mail_settings(self):
        return {
            "MAIL_SERVER": os.getenv('MAIL_SERVER'),
            "MAIL_PORT": 587,
            "MAIL_USE_TLS": True,
            "MAIL_USE_SSL": False,
            "MAIL_USERNAME": os.getenv('MAIL_USERNAME'),
            "MAIL_PASSWORD": os.getenv('MAIL_PASSWORD'),
        }


# App creation and config
app= Flask(__name__)
if production == False:
    config = Config(production=False)
else:
    config = Config(production=True)

db = config.create_db_alchemy(app)
app.config.update(config.set_secret_key())
app.config.update(config.debug())
# Mail confif
app.config.update(config.mail_settings())
mail = Mail(app)

now = datetime.datetime.now()
current_date = now.today().date()
current_year = now.year



