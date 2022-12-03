import math

import cloudinary.uploader
from flask import render_template, request, redirect, session, jsonify, url_for
from app import app, login, utils, models
from app.models import *
from flask_login import login_user, logout_user
from app.decorator import annonynous_user
import cloudinary.uploader
import json

@app.route('/')
def index():
    menu = utils.load_menu()
    return render_template('index.html')



@app.route('/dangKyKham', methods=['get', 'post'])
def dangKyKham(baseModel):
    menu = utils.load_menu()
    err_msg = ''
    diaChi = ''
    hoTen = ''
    namSinh = ''
    gioiTinh = ''
    avatar_path = None
    if request.method.__eq__('POST'):

        hoTen = request.form.get('hoTen')
        namSinh = request.form.get('namSinh')
        diaChi = request.form.get('diaChi')
        gioiTinh = request.form.get('gioiTinh')
        ngayKham = request.form.get('ngayKham')
        avatar = ''
        if request.files:
            res = cloudinary.uploader.upload(request.files['avatar'])
            avatar = res['secure_url']

        try:


            utils.them_benhnhan_cho_duyet(hoTen=hoTen,namSinh=namSinh,diaChi=diaChi,
                                          gioiTinh=gioiTinh,
                                          ngayKham=ngayKham,
                                          avatar=avatar)
            return redirect(url_for(('index')))

        except Exception as ex:
            err_msg = "He thong dang co loi !!!" + str(ex)

    return render_template('dangKyKham.html', err_msg=err_msg)


@app.route('/lapPhieuKham')
def lapPhieuKham():
    menu = utils.load_menu()

    return render_template('lapPhieuKham.html')



@app.route('/duyetDanhSach')
def duyetDanhSach():
    menu = utils.load_menu()
    ngayKhamFind  = request.args.get('ngayKhamFind')
    ngayKhamFind1 = request.args.get('ngayKhamFind1') or ngayKhamFind # lấy cho bên box đã duyệt làm mặc địn ngày giờ render ra
    QueueToAdd = utils.load_QueueToAdd(ngayKham=ngayKhamFind)
    Patient = utils.load_QueueToAdd(ngayKham=ngayKhamFind1)
    return render_template('duyetDanhSach.html',QueueToAdd = QueueToAdd, Patient =Patient, ngayKhamFind = ngayKhamFind)


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

@app.route('/api/listKham', methods = ['post'])
def add_to_listKham():

        data= request.json

        key = app.config['LIST_KHAM_KEY']
        listKham = session.get(key)
        keyByDay = app.config['LIST_KHAM_THEO_NGAY']
        listKhamTheoNgay = session.get(keyByDay)


        id = str(data['id'])
        hoTen = str(data['hoTen'])
        diaChi = str(data['diaChi'])
        namSinh = str(data['namSinh'])
        gioiTinh = str(data['gioiTinh'])
        sdt = str(data['sdt'])
        ngayKham = str(data['ngayKham'])
        avatar = str(data['avatar'])

        listKhamTheoNgay = session[keyByDay] if keyByDay in session else {}
        listKham = session[key] if key in session else {}


        listKhamTheoNgay[ngayKham] = {
            "id": id,
            "hoTen": hoTen,
            "diaChi": diaChi,
            "gioiTinh": gioiTinh,
            "namSinh": namSinh,
            "sdt": sdt,
            "ngayKham": ngayKham,
            "avatar": avatar
        }



        session['listKhamTheoNgay'] = listKhamTheoNgay

        return jsonify(utils.listKhamTheoNgay_stats(listKhamTheoNgay))



@app.context_processor
def common_attribute():
    menu = utils.load_menu()
    return {
        'menu': menu,
        'listKhamTheoNgay': utils.listKhamTheoNgay_stats(session.get(app.config['LIST_KHAM_THEO_NGAY']))

    }


if __name__ == '__main__':
    app.run(debug=True)
