import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ntc-learning-platform-secret-key'

# Konfigurasi database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(basedir), 'instance', 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database
db = SQLAlchemy(app)

# Inisialisasi login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'

# Import models
from src.models.user import User
from src.models.course import Course, Lesson, Quiz, Question, Option
from src.models.progress import UserProgress, UserQuizResult
from src.models.achievement import Achievement, UserAchievement

# Import routes
from src.routes.auth import auth_bp
from src.routes.main import main_bp
from src.routes.learning import learning_bp
from src.routes.scoreboard import scoreboard_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(scoreboard_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

# Route utama
@app.route('/')
def index():
    return redirect(url_for('main.index'))

if __name__ == '__main__':
    app.run(debug=True)
