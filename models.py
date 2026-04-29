from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(255))  # Path to profile picture file
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FighterProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)  # in cm
    walk_around_weight = db.Column(db.Float, nullable=False)  # in lbs
    weight_class = db.Column(db.String(50), nullable=False)
    fight_date = db.Column(db.Date, nullable=False)
    training_availability = db.Column(db.Integer, nullable=False)  # days/week
    se_angle = db.Column(db.String(50), nullable=False)  # Striking, Grappling, Mixed

    user = db.relationship('User', backref=db.backref('fighter_profile', uselist=False))

class CampPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weeks_remaining = db.Column(db.Integer, nullable=False)
    fight_type = db.Column(db.String(50), nullable=False)  # 3 rounds, 5 rounds
    opponent_name = db.Column(db.String(100), nullable=True)  # Optional opponent name
    opponent_strengths = db.Column(db.Text, nullable=True)  # Opponent's strengths
    opponent_weaknesses = db.Column(db.Text, nullable=True)  # Opponent's weaknesses
    plan_phases = db.Column(db.Text, nullable=False)  # JSON string of phases
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('camp_plans', lazy=True))

class GamePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opponent_name = db.Column(db.String(150))  # Name of opponent from Fighter database
    opponent_strengths = db.Column(db.Text, nullable=False)
    opponent_weaknesses = db.Column(db.Text, nullable=False)
    preferred_range = db.Column(db.String(50), nullable=False)  # Striking, Grappling
    round_objectives = db.Column(db.Text, nullable=False)  # JSON string of round-by-round
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('game_plans', lazy=True))

class WeightLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # in lbs

    user = db.relationship('User', backref=db.backref('weight_logs', lazy=True))

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_requests', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_requests', lazy=True))

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user1 = db.relationship('User', foreign_keys=[user1_id], backref=db.backref('friendships1', lazy=True))
    user2 = db.relationship('User', foreign_keys=[user2_id], backref=db.backref('friendships2', lazy=True))


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_messages', lazy=True))

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(100))
    weight_class = db.Column(db.String(50), nullable=False)
    record = db.Column(db.String(20))  # e.g., "15-5-0"
    fighting_style = db.Column(db.String(100))  # Striking, Grappling, Mixed, etc.
    strengths = db.Column(db.Text)  # Comma-separated strengths
    weaknesses = db.Column(db.Text)  # Comma-separated weaknesses
    notable_fights = db.Column(db.Text)  # Notable wins/losses
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SparringProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)  # City, State/Country
    latitude = db.Column(db.Float)  # For location-based matching
    longitude = db.Column(db.Float)  # For location-based matching
    skill_level = db.Column(db.String(50), nullable=False)  # Beginner, Intermediate, Advanced, Expert
    preferred_styles = db.Column(db.Text, nullable=False)  # Comma-separated: Striking, Grappling, Mixed, etc.
    availability = db.Column(db.Text, nullable=False)  # JSON string of available days/times
    max_distance = db.Column(db.Integer, default=50)  # Max distance in miles/km for matches
    self_skill_rating = db.Column(db.Integer, default=5)  # 1-10 scale, self-assessed
    honesty_score = db.Column(db.Float, default=1.0)  # Honesty multiplier based on assessment validation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('sparring_profile', uselist=False))

class SparringSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, completed
    session_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)  # Additional notes about the session
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    requester = db.relationship('User', foreign_keys=[requester_id], backref=db.backref('requested_sessions', lazy=True))
    partner = db.relationship('User', foreign_keys=[partner_id], backref=db.backref('partner_sessions', lazy=True))

class SkillAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sparring_session.id'), nullable=False)
    assessor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Who gave the assessment
    assessed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Who was assessed
    skill_rating = db.Column(db.Integer, nullable=False)  # 1-10 scale
    assessment_notes = db.Column(db.Text)  # Detailed feedback
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    session = db.relationship('SparringSession', backref=db.backref('assessments', lazy=True))
    assessor = db.relationship('User', foreign_keys=[assessor_id], backref=db.backref('given_assessments', lazy=True))
    assessed = db.relationship('User', foreign_keys=[assessed_id], backref=db.backref('received_assessments', lazy=True))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # Amateur, Semi-Pro, Professional, Open
    date = db.Column(db.DateTime, nullable=False)
    registration_deadline = db.Column(db.DateTime)
    location = db.Column(db.String(255), nullable=False)
    venue_name = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    country = db.Column(db.String(100), default='USA')
    weight_classes = db.Column(db.Text, nullable=False)  # Comma-separated weight classes
    experience_levels = db.Column(db.Text, nullable=False)  # Comma-separated: Beginner, Intermediate, Advanced
    rules = db.Column(db.String(100))  # MMA, Boxing, Muay Thai, BJJ, Wrestling, Kickboxing
    entry_fee = db.Column(db.Float, default=0)
    prize_info = db.Column(db.Text)
    contact_email = db.Column(db.String(150))
    contact_phone = db.Column(db.String(50))
    website = db.Column(db.String(255))
    max_participants = db.Column(db.Integer)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=True)  # For moderation if needed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organizer = db.relationship('User', backref=db.backref('organized_events', lazy=True))

    def get_weight_classes_list(self):
        return [wc.strip() for wc in self.weight_classes.split(',') if wc.strip()]
    
    def get_experience_levels_list(self):
        return [el.strip() for el in self.experience_levels.split(',') if el.strip()]


class EventInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(30), default='interested')  # interested, registered, withdrawn
    weight_class = db.Column(db.String(50))  # The weight class they want to compete in
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship('Event', backref=db.backref('interests', lazy=True))
    user = db.relationship('User', backref=db.backref('event_interests', lazy=True))
