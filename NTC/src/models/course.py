from datetime import datetime
from src.main import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Relationships
    quiz = db.relationship('Quiz', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')
    progress = db.relationship('UserProgress', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    points = db.Column(db.Integer, default=10)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    results = db.relationship('UserQuizResult', backref='quiz', lazy='dynamic')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    # Relationships
    options = db.relationship('Option', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Question {self.id}>'

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    def __repr__(self):
        return f'<Option {self.id}>'
