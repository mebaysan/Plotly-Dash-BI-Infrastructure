from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flaskapp.models.user import UserModel, RoleModel
from flaskapp.models.utilities.models import AyModel
from flaskapp.db import db
app = Blueprint('admin', __name__)


@app.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    return render_template('admin/index.jinja2')


@app.route('/users/', methods=['GET'])
@login_required
def users():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    users = UserModel.get_all()
    return render_template('admin/users.jinja2', users=users)


@app.route('/users/add', methods=['POST'])
@login_required
def user_add():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = True if request.form.get('is_admin') == 'True' else False
    if UserModel.find_by_username(username):
        flash(f'{username} Zaten mevcut! Başka bir kullanıcı adı deneyin', 'warning')
        return redirect(url_for('admin.index'))
    new_user = UserModel(
        username=username, password=password, is_admin=is_admin)
    new_user.set_password(password)
    new_user.save_to_db()
    flash(f'{username} Kullanıcısı başarıyla eklendi!', 'success')
    return redirect(url_for('admin.users'))


@app.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def user_delete(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    user = UserModel.find_by_id(id)
    user.delete_from_db()
    flash(f'{user.username} Kullanıcısı başarıyla silindi!', 'success')
    return redirect(url_for('admin.users'))


@app.route('/users/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def user_detail(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    user = UserModel.find_by_id(id)
    roles = RoleModel.get_all()
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.is_admin = True if request.form.get(
            'is_admin') == 'True' else False
        if request.form.get('password'):
            user.set_password(request.form.get('password'))
        user.roles.clear()
        roles = request.form.getlist('roles')
        for role in roles:
            user.roles.append(RoleModel.find_by_id(role))
        user.save_to_db()
        flash(f'{user.username} Başarıyla güncellendi!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/user_detail.jinja2', user=user, roles=roles)


@app.route('/roles/', methods=['GET'])
@login_required
def roles():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    roles = RoleModel.get_all()
    return render_template('admin/roles.jinja2', roles=roles)


@app.route('/roles/add', methods=['POST'])
@login_required
def role_add():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    role_name = request.form.get('role_name')
    if RoleModel.find_by_name(role_name):
        flash(f'{role_name} Zaten mevcut! Başka bir rol adı deneyin', 'warning')
        return redirect(url_for('admin.index'))
    new_role = RoleModel(role_name)
    new_role.save_to_db()
    flash(f'{new_role.name} Rolü başarıyla eklendi!', 'success')
    return redirect(url_for('admin.roles'))


@app.route('/roles/delete/<int:id>', methods=['POST'])
@login_required
def role_delete(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    role = RoleModel.find_by_id(id)
    role.delete_from_db()
    flash(f'{role.name} Rolü başarıyla silindi!', 'success')
    return redirect(url_for('admin.roles'))


@app.route('/roles/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def role_detail(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    role = RoleModel.find_by_id(id)
    users = UserModel.get_all()
    if request.method == 'POST':
        role.name = request.form.get('newRoleName')
        role.users.clear()
        users = request.form.getlist('roleUsers')
        for user in users:
            role.users.append(UserModel.find_by_id(user))
        role.save_to_db()
        flash(f'{role.name} Rolü başarıyla güncellendi!', 'success')
        return redirect(url_for('admin.role_detail',id=id))
    return render_template('admin/role_detail.jinja2', role=role, users=users)


@app.route('/login-logs/')
@login_required
def login_logs():
    query = db.session.execute('select * from user_login;')
    return render_template('admin/login_logs.jinja2', query=query)


@app.route('/months/', methods=['GET'])
@login_required
def months():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    months = AyModel.get_all()
    return render_template('admin/months.jinja2', months=months)


@app.route('/months/add', methods=['POST'])
@login_required
def month_add():
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    month_name = request.form.get('month_name')
    if AyModel.find_by_name(month_name):
        flash(f'{month_name} Zaten mevcut! Başka bir ay adı deneyin', 'warning')
        return redirect(url_for('admin.index'))
    new_ay = AyModel(month_name)
    new_ay.save_to_db()
    flash(f'{new_ay.name} Ayı başarıyla eklendi!', 'success')
    return redirect(url_for('admin.months'))


@app.route('/months/delete/<int:id>', methods=['POST'])
@login_required
def month_delete(id):
    if not current_user.is_admin:
        flash('Bu sayfayı görüntülemek için gerekli izne sahip değilsiniz', 'warning')
        return redirect(url_for('index'))
    month = AyModel.find_by_id(id)
    month.delete_from_db()
    flash(f'{month.name} Ayı başarıyla silindi!', 'success')
    return redirect(url_for('admin.months'))
