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




def load_QueueToAdd(ngayKham = None):
    queue = QueueToAdd.query.all()
    if ngayKham:
        queue = QueueToAdd.query.filter(QueueToAdd.ngayKham.__eq__(ngayKham) )


    return queue
def load_menu():
    return read_json(os.path.join(app.root_path, 'data/menu.json'))


def them_benhnhan_cho_duyet(hoTen, namSinh, diaChi, gioiTinh,ngayKham,sdt, avatar):
    p1 = QueueToAdd(hoTen=hoTen, namSinh=namSinh, diaChi=diaChi, sdt = sdt, gioiTinh=gioiTinh,ngayKham = ngayKham,avatar = avatar)
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


def add_patient(listKhamTheoNgay):
    if listKhamTheoNgay:

        for c in listKhamTheoNgay.values():
            d = Patient(name=c['hoTen'],
                        id=c['id'],
                        sex=c['gioiTinh'],
                        birthday = str(datetime.strptime(c['namSinh'], '%Y-%m-%d')).strftime('%Y-%m-%d'),
                        address = c['diaChi'],
                        dateKham = str(datetime.strptime(c['ngayKham'], '%Y-%m-%d')),
                        avatar = c['avatar'],
                        phone = c['sdt'])
            db.session.add(d)

        db.session.commit()

def add_patientV2(listKhamTheoNgay):
    if listKhamTheoNgay:

        for c in listKhamTheoNgay.values():
            d = Patient(
                        id=c['id'],
                        name=c['hoTen'],

                        sex=c['gioiTinh'],
                        birthday = str(datetime.strptime(c['namSinh'], '%Y-%m-%d')).strftime('%Y-%m-%d'),
                        address = c['diaChi'],
                        dateKham = str(datetime.strptime(c['ngayKham'], '%Y-%m-%d')).strftime('%Y-%m-%d'),
                        avatar = c['avatar'],
                        phone = c['sdt'])
            db.session.add(d)

        db.session.commit()

def load_patient(ngayKham):
    patient = Patient.query.all()
    if ngayKham:
        patient = Patient.query.filter(QueueToAdd.ngayKham.__eq__(ngayKham) )


    return patient
def load_session(ngayKham = None):
    listKhamTheoNgay = session.get(app.config['LIST_KHAM_THEO_NGAY'])
    listKham = []
    if listKhamTheoNgay:
        for i  in listKhamTheoNgay.values():
            if i['ngayKham'] == ngayKham:
                listKham.append(i)
    return listKham

def count_patient():
    return db.session.query(Patient.id, func.count(Patient.id)) \
      .all()
def listKhamTheoNgay_stats(listKhamTheoNgay, ngayKhamFind = None):
    total_amount = 0

    if listKhamTheoNgay:
            for b in listKhamTheoNgay.values():
                total_amount += 1

    return  {'total_amount': total_amount}
