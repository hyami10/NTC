from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.main import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    total_score = db.Column(db.Integer, default=0)
    
    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic')
    quiz_results = db.relationship('UserQuizResult', backref='user', lazy='dynamic')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_score(self, points):
        self.total_score += points
        db.session.commit()
    
    def get_progress(self, course_id):
        return UserProgress.query.filter_by(user_id=self.id, course_id=course_id).first()
    
    def get_completed_lessons(self):
        return [progress.lesson_id for progress in self.progress.filter_by(completed=True)]
    
    def get_completed_courses(self):
        completed_courses = []
        courses = Course.query.all()
        for course in courses:
            lessons = Lesson.query.filter_by(course_id=course.id).all()
            lesson_ids = [lesson.id for lesson in lessons]
            completed_lesson_ids = self.get_completed_lessons()
            if all(lesson_id in completed_lesson_ids for lesson_id in lesson_ids):
                completed_courses.append(course.id)
        return completed_courses
    
    def __repr__(self):
        return f'<User {self.username}>'
