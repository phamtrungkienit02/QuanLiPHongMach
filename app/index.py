import math

import cloudinary.uploader
from flask import render_template, request, redirect, session, jsonify, url_for
from app import app, login, utils, models
from datetime import date, datetime

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
def dangKyKham():
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
        sdt = request.form.get("sdt")
        avatar = ''
        if request.files:
            res = cloudinary.uploader.upload(request.files['avatar'])
            avatar = res['secure_url']

        try:


            utils.them_benhnhan_cho_duyet(hoTen=hoTen,namSinh=namSinh,diaChi=diaChi,
                                          gioiTinh=gioiTinh,
                                          ngayKham=ngayKham,
                                          avatar=avatar, sdt= sdt)
            ok = 'chúc mừng bạn đã đăng ký xong, bây giờ chờ y tá duyệt danh sách'
            # return redirect(url_for(('index')))
            return render_template('index.html', ok = ok)
        except Exception as ex:
            err_msg = "He thong dang co loi !!!" + str(ex)

    return render_template('dangKyKham.html', err_msg=err_msg)



@app.route('/api/saveList', methods=['get', 'post'])
def save_list():
    key = app.config['LIST_KHAM_THEO_NGAY']
    listKhamTheoNgay = session.get(key)

    try:
        utils.add_patient(listKhamTheoNgay = listKhamTheoNgay)
    except:
        return jsonify({'status': 500})
    else:
        del session[key]
        return jsonify({'status': 200})



@app.route('/lapPhieuKham', methods=['post', 'get'])
def lapPhieuKham():
    menu = utils.load_menu()
    err_msg = ''
    diaChi = ''
    hoTen = ''
    namSinh = ''
    gioiTinh = ''
    avatar_path = None
    patient = []
    maBenhNhan = 1
    id_in_patient = False
    ok = "Bác sỹ đã lập thành công 1 phiếu khám!!!"

    if request.method.__eq__('GET'):
        maBenhNhan = request.args.get('maBenhNhan')
        patient = []
        patient = utils.load_patient(id = maBenhNhan)
        if patient is not []:
             id_in_patient = True  # true or false

    if request.method.__eq__('POST'):
        err_msg = "co post"
        maBenhNhanByPost = request.form.get('maBenhNhanByPost')

        namSinh = request.form.get('namSinh') # vì đã có mã patient nên ô này ko cần
        diaChi = request.form.get('diaChi') # vì đã có mã patient nên ô này ko dùng
        trieuChung = request.form.get('trieuChung')
        cachDung = request.form.get('cachDung')
        duDoanBenhLy = request.form.get('duDoanBenhLy')
        maThuoc = request.form.get('maThuoc')
        donVi = request.form.get('donVi')
        soLuong = request.form.get('soLuong')

        try:
            utils.them_lapphieukham(maBenhNhanByPost = maBenhNhanByPost,
                                          trieuChung = trieuChung,
                                          duDoanBenhLy=duDoanBenhLy,
                                            cachDung = cachDung,
                                          maThuoc=maThuoc, donVi = donVi, soLuong = soLuong)

            return render_template('index.html', ok = ok)
        except Exception as ex:
            err_msg = "He thong dang co loi !!!" + str(ex)


    return render_template('lapPhieuKham.html', err_msg=err_msg, patient = patient, id_in_patient = id_in_patient)



@app.route('/duyetDanhSach', methods=['post', 'get'])
def duyetDanhSach():
    menu = utils.load_menu()
    ngayKhamFind = request.args.get('ngayKhamFind')
    ngayKhamFind1 = request.args.get('ngayKhamFind1') or ngayKhamFind# lấy cho bên box đã duyệt làm mặc địn ngày giờ render ra
    QueueToAdd = utils.load_QueueToAdd(ngayKham=ngayKhamFind)

    dt = '2022-4-5'
    dt1 = '2022-2-2'



    date_format = '%Y-%m-%d'

    listKham = []
    Patient = []
    if ngayKhamFind:
        dt = datetime.strptime(ngayKhamFind, date_format)
    if ngayKhamFind1:
        dt1 = datetime.strptime(ngayKhamFind1, date_format)
        listKham = utils.load_session(dt1)

        Patient = utils.load_patient(ngayKham=dt1.strftime(date_format))

    # for i  in Patient:
    #     kieu = type(i.dateKham)
        # key = app.config['LIST_KHAM_THEO_NGAY']
        # if key in session:
        #     del session[key]


    return render_template('duyetDanhSach.html',QueueToAdd = QueueToAdd, Patient = Patient,
                           ngayKhamFind = dt ,
                           ngayKhamFind1 = dt1, listKham = listKham
                           )


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
    key = app.config['LIST_KHAM_THEO_NGAY']
    if key in session:
        del session[key]
    return redirect('/dangNhap')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


# @app.route('/admin')
# def admin():
#     # menu = utils.load_menu()
#
#    # return render_template('admin/index.html')
#     return redirect('/admin')


@app.route('/api/listKham', methods = ['post'])
def add_to_listKham():

        data= request.json

        key = app.config['LIST_KHAM_KEY']
        listKham = session.get(key)
        keyByDay = app.config['LIST_KHAM_THEO_NGAY']
        listKhamTheoNgay = session.get(keyByDay)

        id = str(data['id'])
        hoTen = data['hoTen']
        diaChi = data['diaChi']
        namSinh = data['namSinh']
        gioiTinh = data['gioiTinh']
        sdt = data['sdt']

        ngayKham = data['ngayKham']
        avatar = data['avatar']
        listKhamTheoNgay = session[keyByDay] if keyByDay in session else {}

            # co id trong patient ko cho them
        listKhamTheoNgay[id] = {
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



@app.route("/detail_patient/<int:QueueToAdd_id>")
def details(QueueToAdd_id):
    menu = utils.load_menu()

    q = utils.get_QueueToAdd_by_id(QueueToAdd_id)
    return render_template('detail_patient.html', QueueToAdd= q, menu = menu)

@app.context_processor
def common_attribute():
    menu = utils.load_menu()
    return {
        'menu': menu,
        'listKhamTheoNgay': utils.listKhamTheoNgay_stats(session.get(app.config['LIST_KHAM_THEO_NGAY']))

    }


@app.route('/admin-login', methods=['post'])
def sigin_admin():
        err_msg = ''
        username = request.form['username']
        password = request.form['password']

        user = utils.check_admin(username=username,
                                 password=password,
                                 role="ADMIN")
        if user:
            login_user(user=user)

        else:
            err_mgs = "Tài khoản hoặc mật khẩu không chính xác"
        return redirect('/admin')

@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    #kiem tra get hay post
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            #kiem tra mat khau confirm
            if password.strip().__eq__(confirm.strip()):
                #chu y: avatar la files khong phai form
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username,
                               password=password, email=email,
                               avatar=avatar_path)
                return redirect(url_for('login_my_user'))

            else:
                err_msg = 'Mật khẩu không khớp!!!'
        except Exception as ex:
            err_msg = "Hệ thống có lỗi: " + str(ex)

    return render_template('register.html', err_msg=err_msg)

if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)
