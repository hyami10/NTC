from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from src.models.course import Course
from src.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Halaman utama website"""
    courses = Course.query.order_by(Course.order).all()
    
    # Ambil 5 user dengan skor tertinggi untuk scoreboard mini
    top_users = User.query.order_by(User.total_score.desc()).limit(5).all()
    
    return render_template('index.html', 
                          courses=courses, 
                          top_users=top_users)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Halaman dashboard untuk user yang sudah login"""
    # Ambil progress user
    completed_lessons = current_user.get_completed_lessons()
    completed_courses = current_user.get_completed_courses()
    
    # Ambil semua course
    courses = Course.query.order_by(Course.order).all()
    
    # Hitung progress
    total_lessons = sum(course.lessons.count() for course in courses)
    progress_percent = 0
    if total_lessons > 0:
        progress_percent = (len(completed_lessons) / total_lessons) * 100
    
    return render_template('dashboard.html', 
                          courses=courses,
                          completed_lessons=completed_lessons,
                          completed_courses=completed_courses,
                          progress_percent=progress_percent)

@main_bp.route('/about')
def about():
    """Halaman tentang website"""
    return render_template('about.html')
