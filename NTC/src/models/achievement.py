from datetime import datetime
from src.main import db

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge_image = db.Column(db.String(100), nullable=True)
    points = db.Column(db.Integer, default=10)
    
    # Relationships
    users = db.relationship('UserAchievement', backref='achievement', lazy='dynamic')
    
    def __repr__(self):
        return f'<Achievement {self.title}>'

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserAchievement user_id={self.user_id} achievement_id={self.achievement_id}>'
