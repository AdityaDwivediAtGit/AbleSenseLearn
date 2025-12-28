from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    """User model for authentication and user data"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    full_name = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='student')  # student, teacher, admin, parent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    accessibility_profile = db.relationship('AccessibilityProfile', 
                                          backref='user', 
                                          uselist=False,
                                          cascade='all, delete-orphan')
    learning_profile = db.relationship('LearningProfile',
                                      backref='user',
                                      uselist=False,
                                      cascade='all, delete-orphan')
    contents = db.relationship('Content', backref='author', lazy='dynamic')
    interactions = db.relationship('UserInteraction', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class AccessibilityProfile(db.Model):
    """Accessibility preferences and needs for users"""
    __tablename__ = 'accessibility_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Disability information
    disability_type = db.Column(db.String(50))  # dyslexia, low_vision, hearing_impairment, motor, autism, adhd, none
    disability_severity = db.Column(db.String(20))  # mild, moderate, severe
    
    # Visual preferences
    preferred_font = db.Column(db.String(50), default='Arial')
    preferred_font_size = db.Column(db.Integer, default=16)
    line_spacing = db.Column(db.Float, default=1.5)
    letter_spacing = db.Column(db.Float, default=0.0)
    high_contrast_mode = db.Column(db.Boolean, default=False)
    color_blind_mode = db.Column(db.String(20))  # protanopia, deuteranopia, tritanopia
    
    # Content preferences
    requires_simplified_text = db.Column(db.Boolean, default=False)
    simplification_level = db.Column(db.String(20), default='intermediate')  # basic, intermediate, advanced
    requires_alt_text = db.Column(db.Boolean, default=True)
    prefers_audio = db.Column(db.Boolean, default=False)
    prefers_video = db.Column(db.Boolean, default=False)
    
    # Assistive technology
    text_to_speech_enabled = db.Column(db.Boolean, default=False)
    speech_rate = db.Column(db.Float, default=1.0)  # 0.5 to 2.0
    screen_reader_enabled = db.Column(db.Boolean, default=False)
    uses_braille = db.Column(db.Boolean, default=False)
    
    # Navigation preferences
    keyboard_navigation = db.Column(db.Boolean, default=True)
    voice_commands = db.Column(db.Boolean, default=False)
    reduced_motion = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AccessibilityProfile user:{self.user_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'disability_type': self.disability_type,
            'disability_severity': self.disability_severity,
            'visual': {
                'preferred_font': self.preferred_font,
                'preferred_font_size': self.preferred_font_size,
                'line_spacing': self.line_spacing,
                'letter_spacing': self.letter_spacing,
                'high_contrast_mode': self.high_contrast_mode,
                'color_blind_mode': self.color_blind_mode
            },
            'content': {
                'requires_simplified_text': self.requires_simplified_text,
                'simplification_level': self.simplification_level,
                'requires_alt_text': self.requires_alt_text,
                'prefers_audio': self.prefers_audio,
                'prefers_video': self.prefers_video
            },
            'assistive_tech': {
                'text_to_speech_enabled': self.text_to_speech_enabled,
                'speech_rate': self.speech_rate,
                'screen_reader_enabled': self.screen_reader_enabled,
                'uses_braille': self.uses_braille
            },
            'navigation': {
                'keyboard_navigation': self.keyboard_navigation,
                'voice_commands': self.voice_commands,
                'reduced_motion': self.reduced_motion
            }
        }

class LearningProfile(db.Model):
    """Learning preferences and history for users"""
    __tablename__ = 'learning_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Learning style (multiple can be true)
    learning_style = db.Column(db.String(20))  # visual, auditory, kinesthetic, reading_writing
    pace = db.Column(db.String(20), default='moderate')  # slow, moderate, fast
    preferred_modality = db.Column(db.String(50))  # text, audio, video, interactive, mixed
    
    # Academic information
    grade_level = db.Column(db.String(20))
    subjects_of_interest = db.Column(db.Text)  # JSON string of subjects
    strengths = db.Column(db.Text)  # JSON string of strengths
    challenges = db.Column(db.Text)  # JSON string of challenges
    
    # Accommodations
    accommodations = db.Column(db.Text)  # JSON string of accommodations
    
    # Performance metrics
    average_comprehension_score = db.Column(db.Float, default=0.0)
    average_engagement_score = db.Column(db.Float, default=0.0)
    preferred_session_length = db.Column(db.Integer, default=30)  # minutes
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningProfile user:{self.user_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        import json
        return {
            'user_id': self.user_id,
            'learning_style': self.learning_style,
            'pace': self.pace,
            'preferred_modality': self.preferred_modality,
            'grade_level': self.grade_level,
            'subjects_of_interest': json.loads(self.subjects_of_interest) if self.subjects_of_interest else [],
            'strengths': json.loads(self.strengths) if self.strengths else [],
            'challenges': json.loads(self.challenges) if self.challenges else [],
            'accommodations': json.loads(self.accommodations) if self.accommodations else [],
            'performance': {
                'average_comprehension_score': self.average_comprehension_score,
                'average_engagement_score': self.average_engagement_score,
                'preferred_session_length': self.preferred_session_length
            }
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))