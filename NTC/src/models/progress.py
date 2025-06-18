from datetime import datetime
from src.main import db

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserProgress user_id={self.user_id} lesson_id={self.lesson_id}>'

class UserQuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    max_score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserQuizResult user_id={self.user_id} quiz_id={self.quiz_id} score={self.score}>'
