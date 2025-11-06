from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, limiter, login_manager
from ..models import User
from ..forms.auth_forms import LoginForm, RegisterForm, ResetPasswordForm

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# ✅ LOGIN — limiter exempt (no more Too Many Requests)
@bp.route('/login', methods=['GET','POST'])
@limiter.exempt
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard.home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


# ✅ REGISTER — limiter exempt
@bp.route('/register', methods=['GET','POST'])
@limiter.exempt
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username exists', 'danger')
        else:
            user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))


# ✅ RESET PASSWORD — limiter exempt
@bp.route('/reset-password', methods=['GET','POST'])
@limiter.exempt
def reset_password():
    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('User not found', 'danger')
        else:
            user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password reset successfully!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
