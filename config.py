import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('CONN_STRPG')
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True