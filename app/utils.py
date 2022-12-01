import json, os
from app import app, db
from app import models
from app.models import *
import hashlib
import data
from flask_login import current_user


def read_json(path):
    with open(path, "r", encoding='utf8') as f:
        return json.load(f)


def load_categories():
    return read_json(os.path.join(app.root_path, 'data/categories/json'))


def load_products():
    return read_json(os.path.join(app.root_path, 'data/products.json'))


def load_menu():
    return read_json(os.path.join(app.root_path, 'data/menu.json'))


def them_benhnhan_cho_duyet(hoTen="Tom", namSinh=2 / 3 / 2022, diaChi="diaChiMacDinh", gioiTinh="gay"):
    p1 = QueueToAdd(hoTen=hoTen, namSinh=namSinh, diaChi=diaChi, gioiTinh=gioiTinh)
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

    return menuOfUser


def get_user_by_id(user_id):
    return User.query.get(user_id)


def cart_stats(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity

    }
