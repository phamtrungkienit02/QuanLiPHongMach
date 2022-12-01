import math

from flask import render_template, request, redirect, session, jsonify, url_for
from app import app, login, utils, models
from app.models import *
from flask_login import login_user, logout_user
from app.decorator import annonynous_user


@app.route('/')
def index():
    menu = utils.load_menu()
    return render_template('index.html', menu=menu)


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json
    # data nhận kiểu từ điển tương tự với json

    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    id = str(data['id'])
    name = data['name']
    price = data['price']

    if id in cart:
        cart[id]['quantity'] += 1

    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart
    return jsonify(utils.cart_stats(cart))


@app.route('/dangKyKham', methods=['get', 'post'])
def dangKyKham():
    menu = utils.load_menu()
    err_msg = ''
    diaChi = ''
    hoTen = ''
    namSinh = ''
    gioiTinh = ''
    if request.method.__eq__('POST'):
        hoTen = request.form.get('hoTen')
        namSinh = request.form.get('namSinh')
        diaChi = request.form.get('diaChi')
        gioiTinh = request.form.get('gioiTinh')
        try:

            utils.them_benhnhan_cho_duyet(hoTen=hoTen, namSinh=namSinh, diaChi=diaChi, gioiTinh=gioiTinh)
            return redirect(url_for(('index')))

        except Exception as ex:
            err_msg = "He thong dang co loi !!!" + str(ex)

    return render_template('dangKyKham.html', menu=menu, err_msg=err_msg)


@app.route('/lapPhieuKham')
def lapPhieuKham():
    menu = utils.load_menu()

    return render_template('lapPhieuKham.html', menu=menu)


@app.route('/bacsy')
def bacsy():
    menu = utils.load_menu()
    return render_template('bacsy.html', menu=menu)


@app.route('/yta')
def yta():
    menu = utils.load_menu()
    return render_template('yta.html', menu=menu)


@app.route('/nvtn')
def nvtn():
    menu = utils.load_menu()
    return render_template('nvtn.html', menu=menu)


@app.route('/duyetDanhSach')
def duyetDanhSach():
    menu = utils.load_menu()

    return render_template('duyetDanhSach.html', menu=menu)


@app.route('/thanhToan')
def thanhToan():
    menu = utils.load_menu()

    return render_template('thanhToan.html', menu=menu)


@app.route('/dangNhap', methods=["get", "post"])
def login_my_user():
    menu = utils.load_menu()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.auth_user(username=username, password=password)
        menuOfUser = utils.check_kind_user_to_render_menu()

        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')

        # if user.user_role == UserRole.BACSY:
        #
        #     return redirect(n if n else '/bacsy')
        # if user.user_role == UserRole.YTA:
        #
        #     return redirect(n if n else '/yta')
        # if user.user_role == UserRole.NVTN:
        #
        #     return redirect(n if n else '/nvtn')
        # if user.user_role == UserRole.USER:
        #
        #     return redirect(n if n else '/')

    return render_template('dangNhap.html', menu = menu)


@app.route('/dangXuat')
def logout_my_user():
    logout_user()
    return redirect('/dangNhap')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


@app.route('/admin')
def admin():
    menu = utils.load_menu()

    return render_template('admin.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
