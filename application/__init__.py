from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Application
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1200
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Mention the routes
from application import routes