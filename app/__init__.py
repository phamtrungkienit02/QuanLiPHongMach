from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "djfkhshfu9ggt3yu28y72646y@123D"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/quanliphongmachdb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config['KEY_SAVE_PATIENT'] = 'keySavePatient'
app.config['LIST_KHAM_THEO_NGAY'] = 'listKhamTheoNgay'
db = SQLAlchemy(app = app)

login = LoginManager(app = app)

cloudinary.config(
    cloud_name = 'dibadhds0',
    api_key= '652849689643788',
    api_secret= '0AONEGKZcaQaRdwEAD3PueVv6G8'
)

