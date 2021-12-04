"""the main Flask app"""
from flask import render_template, request, redirect, url_for, flash, Response
from flask import current_app as app
from flask_login import current_user, login_required, login_user, logout_user
import pandas as pd
from flaskapp.dashboard.urls import URL_PATHS
from flaskapp.models.user import UserModel, RoleModel, LoginLog
from flaskapp.db import db
from flaskapp.login import login
from flaskapp.admin.app import app as admin_bp
from datetime import datetime
import pytz
import os
from flaskapp.models.file import FileModel


@app.before_first_request  # uygulamaya ilk istek atılmadan önce
def create_tables():
    db.create_all()


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


@login.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.jinja2', title='Anasayfa')


@app.route('/dashboard/<string:dash_url>')
@login_required
def get_dash(dash_url):
    CONFIG = next(filter(lambda x: x['APP_URL'] == dash_url, URL_PATHS),
                  None)  # URL_PATHS'i gez eşleşen ilk değeri ver yoksa None dön
    if not CONFIG:
        flash('Aradığınız Dashboard bulunamadı', 'danger')
        return redirect(url_for('index'))
    role = RoleModel.find_by_name(dash_url)
    if current_user.is_my_role(role):
        return render_template('dashboards/dashboard_basic.jinja2', dash_url=CONFIG['BASE_URL'], title=CONFIG['APP_NAME'])
    else:
        flash('Bu dashboardu görmek için yetkiye sahip değilsiniz', 'warning')
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.find_by_username(username)
        if user is None or not user.check_password(password):
            flash('Kullanıcı Adı veya Parola Hatalı!', 'danger')
            return render_template('login.jinja2', title='Giriş')
        login_user(user)
        login_log = LoginLog(user.id,
                             datetime.now(pytz.timezone(
                                 'Europe/Istanbul')).now(),
                             datetime.now(pytz.timezone(
                                 'Europe/Istanbul')).date(),
                             datetime.now(pytz.timezone(
                                 'Europe/Istanbul')).time()
                             )
        login_log.save_to_db()
        flash('Başarılı bir şekilde giriş yapıldı', 'success')
        return redirect(url_for('index'))
    return render_template('login.jinja2', title='Giriş')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarılı bir şekilde çıkış yapıldı!', 'success')
    return redirect(url_for('index'))


@app.route('/access/csv/<string:file_slug>')
@login_required
def download_slug_csv(file_slug):
    # buraya hangi url'den istek geldiği
    referrer = request.headers.get("Referer")
    try:
        file_model = FileModel.find_by_slug(file_slug)
        csv = pd.read_csv(file_model.file_full)
        response = Response(csv.to_csv(), mimetype="text/csv", headers={
            "Content-disposition": "attachment; filename={}".format(file_model.file_name)})
        file_model.delete_from_db()
        return response
    except:
        # çok fazla istek geldiğinde dosya okurken hata oluyor, hata olduğunda isteğin geldiği sayfaya dönsün
        return redirect(referrer)


app.register_blueprint(admin_bp, url_prefix='/admin')