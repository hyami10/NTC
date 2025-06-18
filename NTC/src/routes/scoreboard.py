from flask import Blueprint, render_template
from flask_login import current_user
from src.models.user import User
from src.models.course import Course
from src.models.progress import UserProgress

scoreboard_bp = Blueprint('scoreboard', __name__, url_prefix='/scoreboard')

@scoreboard_bp.route('/')
def index():
    """Halaman utama scoreboard"""
    # Ambil semua user dan urutkan berdasarkan total skor (tertinggi ke terendah)
    users = User.query.order_by(User.total_score.desc()).all()
    
    # Hitung jumlah course yang diselesaikan oleh setiap user
    user_stats = []
    for user in users:
        completed_courses = user.get_completed_courses()
        user_stats.append({
            'user': user,
            'completed_courses': len(completed_courses)
        })
    
    return render_template('scoreboard/index.html', 
                          user_stats=user_stats)

@scoreboard_bp.route('/course/<int:course_id>')
def course_scoreboard(course_id):
    """Scoreboard untuk course tertentu"""
    course = Course.query.get_or_404(course_id)
    
    # Ambil semua user yang telah menyelesaikan lesson di course ini
    progress_entries = UserProgress.query.filter_by(course_id=course_id, completed=True).all()
    
    # Hitung jumlah lesson yang diselesaikan oleh setiap user
    user_progress = {}
    for entry in progress_entries:
        if entry.user_id not in user_progress:
            user_progress[entry.user_id] = 0
        user_progress[entry.user_id] += 1
    
    # Ambil data user dan urutkan berdasarkan jumlah lesson yang diselesaikan
    user_stats = []
    for user_id, completed_lessons in user_progress.items():
        user = User.query.get(user_id)
        if user:
            user_stats.append({
                'user': user,
                'completed_lessons': completed_lessons
            })
    
    # Urutkan berdasarkan jumlah lesson yang diselesaikan
    user_stats.sort(key=lambda x: x['completed_lessons'], reverse=True)
    
    return render_template('scoreboard/course.html', 
                          course=course,
                          user_stats=user_stats)
