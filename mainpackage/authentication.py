import functools

from flask import render_template, url_for, redirect, request, flash, g, session, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('authentication', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    from mainpackage import db, User
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = "Please enter an email."

        elif not password:
            error = "Please enter a password."

        if error is None:
            try:
                user = User(email=email, password=generate_password_hash(password), role='student')
                db.session.add(user)
                db.session.commit()
            except db.exc.IntegrityError:
                error = f'User {email} is already registered. Please pick a different email address.'
            else:
                return redirect(url_for('dashboard'))

        flash(error)

    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    from mainpackage import db, User
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = "Please enter an email address."

        elif not password:
            error = "Please enter a password."

        if error is None:
            try:
                user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
            except db.exc.NoResultFound:
                error = 'Incorrect email or password. Please try again.'
            else:
                if check_password_hash(user.password, password) is False:
                    error = 'Incorrect email or password. Please try again.'
                else:
                    session.clear()
                    session['user_id'] = user.user_id
                    return redirect(url_for('dashboard'))
    return render_template('login.html')


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


@bp.before_app_request
def load_logged_in_user():
    from mainpackage import db, User
    try:
        user_id = session.get('user_id')
        user = db.session.execute(db.select(User).filter_by(user_id=user_id)).scalar_one()
    except db.exc.NoResultFound:
        g.User = None
    else:
        g.User = user


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.User is None:
            return redirect(url_for('authentication.login'))
        return view(**kwargs)
    return wrapped_view


# ONLY USE STRINGS for role
def role_required(role):
    def decorate_role(view):
        @functools.wraps(view)
        def wrapped_role(**kwargs):
            if g.User.role != role:
                return redirect(url_for('authentication.login'))
            return view(**kwargs)
        return wrapped_role
    return decorate_role


# ONLY USE STRINGS for role. Not tested
def roles_required(role1, role2):
    def multiple_decorate_role(view):
        @functools.wraps(view)
        def multiple_wrapped_role(**kwargs):
            if g.User.role != role1:
                if g.User.role != role2:
                    return redirect(url_for('authentication.login'))
            return view(**kwargs)
        return multiple_wrapped_role
    return multiple_decorate_role
