from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from app.models import Category, UserRole, Drug, QuiDinhSoLuong, TienKham
from flask_login import current_user, logout_user
from flask import redirect, request
#expose bam vao logout
from flask_admin import BaseView, expose
from datetime import datetime

import utils


#chan bang quyen admin
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)

#authenticatedmodelview past modelview
class ProductView(AuthenticatedModelView):
    #mac dinh khoa chinh bi an
    #de khoa chinh hien
    column_display_pk = True
    #co the xem chi tiet san pham
    can_view_details = True
    #them mot muc export co the xuat ra file excel(mac dinh het cac cot)
    can_export = True
    #them muc tim kiem
    column_searchable_list = ['name', 'description']
    #loc theo filter
    column_filters = ['name', 'price']
    #an cac list
    column_exclude_list = ['image', 'active']
    #doi ten cho cac muc(luu y: viet thuong)
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả sản phẩm',
        'price': 'Giá sản phẩm',
        'image': 'Hình ảnh sản phẩm',
        'category': 'Danh mục'
    }
    #mac dinh cac cot deu co the chinh sort
    #chi dinh sap xep cac list
    column_sortable_list = ['id', 'name', 'price']

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    #dang nhap admin moi thay logout
    def is_accessible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw,
                                                     from_date=from_date,
                                                     to_date=to_date))

    #kiem tra quyen admin
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

#action cua trang admin
class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           stats=utils.category_stats())

#name ten trang admin
admin = Admin(app=app,
              name="E-commerce Administration",
              template_mode='bootstrap4',
              index_view=MyAdminIndex())

#authenticatedmodelview past ModelView
#them db.session vi trang admin co the chinh sua(session la mot bien cua sever can secret key de ma hoa)
admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Drug, db.session))
# admin.add_view(AuthenticatedModelView(QuiDinhSoLuong, db.session))
# admin.add_view(AuthenticatedModelView(TienKham, db.session))
# admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))
