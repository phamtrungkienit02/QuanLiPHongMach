from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime

class BaseModel(db.Model):
    # lenh nay nham khong tao bang trong csdl
    __abstract__ = True
    # kieu int, khoa chinh, tu dong tang
    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(9), nullable=False)
    active = Column(Boolean, default=True)

if __name__ == '__main__':
    with app.app_context():
        #     #tao bang
        db.create_all()


        p1 = User(username='TranVanBe', password='123456789')
        p2 = User(username='TranThiCe', password='abc123ABC')
        p3 = User(username='QUANTHU1', password='PASS123')
        p4 = User(username='admin123', password='admin')

        db.session.add_all([p1, p2, p3, p4])
        # day len server
        db.session.commit()
