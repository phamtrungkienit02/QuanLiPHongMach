import json, os
from datetime import datetime

from app import app, db
from app import models
from app.models import *
import hashlib
from flask_login import current_user
from flask import render_template, request, redirect, session, jsonify, url_for
from sqlalchemy import func


def read_json(path):
    with open(path, "r", encoding='utf8') as f:
        return json.load(f)


def load_categories():
    return read_json(os.path.join(app.root_path, 'data/categories/json'))


def load_products():
    return read_json(os.path.join(app.root_path, 'data/products.json'))


def load_QueueToAdd(ngayKham=None):
    queue = QueueToAdd.query.all()
    if ngayKham:
        queue = QueueToAdd.query.filter(QueueToAdd.ngayKham.__eq__(ngayKham))

    return queue


def load_menu():
    return read_json(os.path.join(app.root_path, 'data/menu.json'))


def them_benhnhan_cho_duyet(hoTen, namSinh, diaChi, gioiTinh, ngayKham, sdt, avatar):
    p1 = QueueToAdd(hoTen=hoTen, namSinh=namSinh, diaChi=diaChi, sdt=sdt, gioiTinh=gioiTinh, ngayKham=ngayKham,
                    avatar=avatar)
    db.session.add(p1)
    db.session.commit()


def them_lapphieukham(maBenhNhanByPost,
                      trieuChung,
                      duDoanBenhLy,
                      cachDung,
                      maThuoc, donVi, soLuong):
    p1 = lapPhieuKhamTB(maBenhNhan=maBenhNhanByPost,
                        trieuChung=trieuChung,
                        duDoanBenhLy=duDoanBenhLy,
                        cachDung=cachDung,
                        maThuoc=maThuoc, donVi=donVi, soLuong=soLuong)
    db.session.add(p1)

    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def check_kind_user_to_render_menu():
    menu = load_menu()
    menuOfUser = []
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.BACSY:

            for i in menu:
                if i.userUse == 'bacsy':
                    menuOfUser.append(i)
        if current_user.user_role == UserRole.YTA:

            for i in menu:
                if i.userUse == 'yta':
                    menuOfUser.append(i)
        if current_user.user_role == UserRole.NVTN:

            for i in menu:
                if i.userUse == 'nvtn':
                    menuOfUser.append(i)
        if current_user.user_role == UserRole.USER:

            for i in menu:
                if i.userUse == 'user':
                    menuOfUser.append(i)
        if current_user.user_role == UserRole.ADMIN:

            for i in menu:
                if i.userUse == 'admin':
                    menuOfUser.append(i)

    return menuOfUser


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_id_in_patient(id=None):
    for i in Patient:
        if int(id).__eq__(int(i.id)):
            return True
    return False


def add_patient(listKhamTheoNgay):
    date_format = '%Y-%m-%d %H:%M:%D'
    if listKhamTheoNgay:

        for c in listKhamTheoNgay.values():
            d = Patient(
                id=c['id'],
                name=c['hoTen'],

                sex=c['gioiTinh'],
                birthday=c['namSinh'],
                address=c['diaChi'],
                dateKham=c['ngayKham'],
                avatar=c['avatar'],
                phone=c['sdt'])
            db.session.add(d)

        db.session.commit()


def add_lapphieukham(listKhamTheoNgay):
    date_format = '%Y-%m-%d %H:%M:%D'
    if listKhamTheoNgay:

        for c in listKhamTheoNgay.values():
            d = Patient(
                id=c['id'],
                name=c['hoTen'],

                sex=c['gioiTinh'],
                birthday=c['namSinh'],
                address=c['diaChi'],
                dateKham=c['ngayKham'],
                avatar=c['avatar'],
                phone=c['sdt'])
            db.session.add(d)

        db.session.commit()


def load_patient(ngayKham=None, id=None):
    patient = Patient.query.all()
    if ngayKham:
        patient = Patient.query.filter(Patient.dateKham.__eq__(ngayKham))
    if id:
        id_songuyen = int(id)
        patient = Patient.query.filter(Patient.id.__eq__(id_songuyen))

    return patient


def load_session(ngayKhamFind=None):
    listKhamTheoNgay = session.get(app.config['LIST_KHAM_THEO_NGAY'])
    listKham = []
    if listKhamTheoNgay:
        for i in listKhamTheoNgay.values():
            ngayKham = datetime.strptime(i['ngayKham'], '%Y-%m-%d %H:%M:%S')
            if ngayKham.year == ngayKhamFind.year and ngayKham.month == ngayKhamFind.month and ngayKham.day == ngayKhamFind.day:
                listKham.append(i)
    return listKham


def get_QueueToAdd_by_id(id):
    return QueueToAdd.query.get(id)


def listKhamTheoNgay_stats(listKhamTheoNgay, ngayKhamFind=None):
    total_amount = 0

    if listKhamTheoNgay:
        for b in listKhamTheoNgay.values():
            total_amount += 1

    return {'total_amount': total_amount}

def check_admin(username, password, role):
    if username and password:
        # luu bam bang thuat toan nao thi kiem tra cung bam bang thuat toan do=> ma bam giong nhau
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        # username lay first vi chi co 1 khong co tra ra null
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()
