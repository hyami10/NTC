from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from src.models.user import User
from src.main import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Email atau password salah', 'danger')
            return render_template('auth/login.html')
        
        login_user(user, remember=remember)
        user.last_login = db.func.now()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash('Login berhasil!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if password != password_confirm:
            flash('Password tidak cocok', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar', 'danger')
            return render_template('auth/register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah logout', 'info')
    return redirect(url_for('main.index'))
