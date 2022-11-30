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
class UserRole(UserEnum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    CASHIER = 4


class Sex(UserEnum):
    MALE = 1
    FEMALE = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    # active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    permission = Column(String(20), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)

    # receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Patient(BaseModel):
    username = Column(String(50), nullable=False, unique=True)
    birthday = Column(DateTime, nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    address = Column(String(50), nullable=False)
    phone = Column(String(11))
    note = Column(String(50))
    # receipts = relationship('Receipt', backref='patient', lazy=True)

class PhieuKham(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    #stt
    #trieuchung
    #chuandoan
    # #maBN
class ToaThuoc(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    #khoaNgoaiPK
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)


# class ReceiptDetail(db.Model):
# receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
# product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
# quantity = Column(Integer, default=0)
# unit_price = Column(Float, default=0)
# class Receipt(db.Model):
#     created_date = Column(DateTime, default=datetime.now())



# class HoaDonThuoc
# created_date = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
#     details = relationship('ReceiptDetail', backref='receipt', lazy=True)

# class ChiTietToaThuoc


class Category(BaseModel):
    __tablename__ = "category"
    name = Column(String(50), nullable=False)
    drugs = relationship('Drug', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Drug(BaseModel):
    __tablename__ = 'drug'
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    unit = Column(String(20), nullable=False)
    create_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        #     #tao bang
        db.create_all()
        # day len server
        db.session.commit()
