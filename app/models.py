from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    runs = db.relationship('Run', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    intro_text = db.Column(db.Text, nullable=False)
    passage = db.Column(db.Text, nullable=False)
    outcome_high = db.Column(db.Text, nullable=False)
    outcome_mid = db.Column(db.Text, nullable=False)
    outcome_low = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_official = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    runs = db.relationship('Run', backref='scenario', lazy=True)

    def __repr__(self):
        return f'<Scenario {self.title}>'

class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'), nullable=False)
    wpm = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    time_remaining = db.Column(db.Integer, nullable=False)
    errors = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    wpm_history = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Run {self.id} by User {self.user_id}>'
    
