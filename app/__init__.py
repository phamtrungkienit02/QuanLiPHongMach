from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = "djfkhshfu9ggt3yu28y72646yu8d6hyufhuift67tf9hyfyuhfuig7dgug"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/TestOnTapdb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config['CART_KEY']  = 'cart'

db = SQLAlchemy(app = app)

login = LoginManager(app = app)

