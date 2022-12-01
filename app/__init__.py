# file khoi dong package

from urllib.parse import quote
from flask import Flask
# database
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
# nhap chuoi khong can qui tac
app.secret_key = '&&^$*JDLSJFosidjfos45454'
# chuoi ket noi den csdl mysql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/librarydb?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/quanliphongmachdb?charset=utf8mb4' % quote('Admin@123')
#bat de khi bo sung thi no thong bao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

cloudinary.config(
    cloud_name='dmjcqxek3',
    api_key='997423884688544',
    api_secret='QMTNUyLzrsOzAocniwM6wI0eTtg'
)

login = LoginManager(app=app)

db = SQLAlchemy(app=app)
