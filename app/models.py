from app import db
from flask_login import UserMixin
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_photo = db.Column(db.String(255), nullable=True, default='profile_photos/default-avatar.svg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    runs = db.relationship('Run', backref='user', lazy=True)

    bot_conversations = db.relationship(

        'BotConversation',

        backref='user',

        lazy=True

    )

    bot_memories = db.relationship(

        'BotMemory',

        backref='user',

        lazy=True

    )

    bot_profile = db.relationship(

        'BotProfile',

        backref='user',

        uselist=False

    )

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


class CampaignProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    mode = db.Column(
        db.String(50),
        nullable=False,
        default='bot'
    )

    world = db.Column(
        db.String(80),
        nullable=False,
        default='xenotype_signal'
    )

    current_node = db.Column(
        db.String(80),
        nullable=False,
        default='intro'
    )

    health = db.Column(
        db.Integer,
        nullable=False,
        default=100
    )

    fear = db.Column(
        db.Integer,
        nullable=False,
        default=10
    )

    confidence = db.Column(
        db.Integer,
        nullable=False,
        default=50
    )

    inventory = db.Column(
        db.Text,
        nullable=False,
        default='[]'
    )

    visited_nodes = db.Column(
        db.Text,
        nullable=False,
        default='[]'
    )

    completed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        'User',
        backref=db.backref('campaign_progress', lazy=True)
    )

    def get_inventory(self):
        try:
            return json.loads(self.inventory or '[]')
        except json.JSONDecodeError:
            return []

    def set_inventory(self, items):
        self.inventory = json.dumps(items)

    def get_visited_nodes(self):
        try:
            return json.loads(self.visited_nodes or '[]')
        except json.JSONDecodeError:
            return []

    def add_visited_node(self, node):
        visited = self.get_visited_nodes()
        visited.append(node)
        self.visited_nodes = json.dumps(visited)

    def reset(self):
        self.mode = 'bot'
        self.world = 'xenotype_signal'
        self.current_node = 'intro'
        self.health = 100
        self.fear = 10
        self.confidence = 50
        self.inventory = '[]'
        self.visited_nodes = '[]'
        self.completed = False

    def __repr__(self):
        return f'<CampaignProgress user_id={self.user_id} node={self.current_node}>'

class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_public = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship(
        'ChatMessage',
        backref='room',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<ChatRoom {self.name}>'


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    room_id = db.Column(
        db.Integer,
        db.ForeignKey('chat_room.id'),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship(
        'User',
        backref=db.backref('chat_messages', lazy=True)
    )

    def to_dict(self):
        return {
            'id': self.id,
            'room': self.room.name if self.room else None,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'Unknown',
            'body': self.body,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

    def __repr__(self):
        return f'<ChatMessage {self.id} by User {self.user_id}>'


class BotConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    player_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

    sentiment = db.Column(db.String(20), default='neutral')

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class BotMemory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(

        db.Integer,

        db.ForeignKey('user.id'),

        nullable=False

    )

    memory_key = db.Column(db.String(100), nullable=False)

    memory_value = db.Column(

        db.Text,

        nullable=False

    )

    importance = db.Column(

        db.Integer,

        default=1

    )

    entity_summary = db.Column(db.Text)

    last_accessed = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )

    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )
    
class BotProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
        unique=True
    )

    friendliness = db.Column(db.Integer, default=50)
    sarcasm = db.Column(db.Integer, default=10)
    helpfulness = db.Column(db.Integer, default=80)

    favorite_topic = db.Column(db.String(100))

    total_messages = db.Column(db.Integer, default=0)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    
class BotKnowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String(100))
    trigger = db.Column(db.String(200))
    response = db.Column(db.Text)

