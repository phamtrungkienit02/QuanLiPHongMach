from sqlalchemy import Column, String, Integer, Float, Enum, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

from app import app, db
class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    BACSY = 3
    YTA = 4  # y tá
    NVTN = 5  # nhân viên thu ngân


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class QueueToAdd(BaseModel):
    __tablename__ = "QueueToAdd"
    hoTen = Column(String(50), nullable=False, default="Anonymous")
    gioiTinh = Column(String(50), nullable=False, default="nam")
    namSinh = Column(DateTime, nullable=False, default='0/0/2002')
    diaChi = Column(String(100))

    def __str__(self):
        return self.hoTen


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False,
                    default="https://vcdn1-giaitri.vnecdn.net/2020/08/18/gdragonava1-1597716430-7452-1597716741.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=dyDAM635cysU8i5PT64U9g")
    active = Column(Boolean, default=True)
    user_role = Column(String(50), default="USER", nullable=False)
    # receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


# kiên
class Sex(UserEnum):
    MALE = 1
    FEMALE = 2

class Patient(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    birthday = Column(DateTime, nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    address = Column(String(50), nullable=False)
    phone = Column(String(11))
    note = Column(String(50))
    prescriptions = relationship('Prescription', backref='patient', lazy=False)
    Anamnesis_details = relationship('AnamnesisDetail', backref='patient', lazy=True)
    def __str__(self):
        return self.name

class MedicalReport(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    stt = Column(Integer, autoincrement=True)
    trieu_chung = Column(String(50), nullable=False)
    chuan_doan = Column(String(50), nullable=False)
    patients = Column(Integer, ForeignKey(Patient.id), nullable=False)
    prescriptions = relationship('Prescription', backref='medicalReport', lazy=False)
    def __str__(self):
        return self.name

class Prescription(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    patients = Column(Integer, ForeignKey(Patient.id), nullable=False)
    medical_reports = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    prescription_details = relationship('PrescriptionDetail', backref='prescription', lazy=True)


class DrugPriceBill(BaseModel):
    create_date = Column(DateTime, nullable=False)
    drug_price = Column(Float, default=0)
    medical_costs = Column(Float, default=50000)
    patients = Column(Integer, ForeignKey(Patient.id), nullable=False)
    prescription_details = relationship('PrescriptionDetail', backref='drugPriceBill', lazy=False)
    def __str__(self):
        return self.name
class Anamnesis(BaseModel):
    anamesis = Column(String(50))
    Anamnesis_details = relationship('AnamnesisDetail', backref='anamesis', lazy=True)

class AnamnesisDetail(db.Model):
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    use_drug = Column(String(50))
    patients = Column(Integer, ForeignKey(Patient.id), nullable=False, primary_key=True)
    anamnesis = Column(Integer, ForeignKey(Anamnesis.id), nullable=False, primary_key=True)

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
    description = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    prescription_details = relationship('PrescriptionDetail', backref='drug', lazy=True)
    def __str__(self):
        return self.name

class PrescriptionDetail(db.Model):
    number = Column(Integer, nullable=False)
    description = Column(String(100))
    prescriptions = Column(Integer, ForeignKey(Prescription.id), nullable=False, primary_key=True)
    drugs = Column(Integer, ForeignKey(Drug.id), nullable=False, primary_key=True)
    drug_price_bills = Column(Integer, ForeignKey(DrugPriceBill.id), nullable=False)


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # import hashlib
        #
        # passwordU1 = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u1 = User(name="Tu09", username="123", password=passwordU1, avatar="./static/img/logo.png", active=True,
        #           user_role="USER")
        #
        # passwordU2 = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u2 = User(name="bacsy1", username="bacsy1", password=passwordU2, avatar="./static/img/logo.png", active=True,
        #           user_role="BACSY")
        #
        # passwordU3 = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u3 = User(name="yta1", username="yta1", password=passwordU3, avatar="./static/img/logo.png", active=True,
        #           user_role="YTA")
        #
        # passwordU4 = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u4 = User(name="nvtn1", username="nvtn1", password=passwordU4, avatar="./static/img/logo.png", active=True,
        #           user_role="NVTN")  # nhân viên thu ngân
        #
        # db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

