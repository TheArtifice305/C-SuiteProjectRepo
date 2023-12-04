from flask import render_template, url_for, redirect, request, flash, Blueprint
from mainpackage import User, db
from mainpackage.authentication import login_required, role_required
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', posts=users)


@bp.route('/create_account', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        message = None

        try:
            user = User(email=email, password=generate_password_hash(password), role=role)
            db.session.add(user)
            db.session.commit()
        except db.exc.IntegrityError:
            message = f'User {email} is already registered. Please pick a different username.'
        else:
            message = f'User {email} is now registered. They will be sent an email with their username, password" \
                      ", and role.'
        flash(message)
    return render_template('admin_create_account.html')


@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_or_delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.email = request.form['email']
        password = request.form['password']
        if password != "":
            user.password = generate_password_hash(password)
        user.role = request.form['role']
        db.session.commit()
        return redirect(url_for('admin.admin'))
    else:
        return render_template('admin_edit_delete_account.html', post=user)


@bp.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.admin'))
