from datetime import datetime
from app import db
import json

class Content(db.Model):
    """Educational content model"""
    __tablename__ = 'content'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content_type = db.Column(db.String(50), nullable=False)  # lesson, quiz, video, article, exercise
    subject = db.Column(db.String(100))
    topic = db.Column(db.String(200))
    difficulty = db.Column(db.String(20), default='intermediate')  # beginner, intermediate, advanced
    body = db.Column(db.Text, nullable=False)  # Main content
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    language = db.Column(db.String(10), default='en')
    
    # Accessibility fields
    has_alt_text = db.Column(db.Boolean, default=False)
    has_captions = db.Column(db.Boolean, default=False)
    has_transcript = db.Column(db.Boolean, default=False)
    has_audio_description = db.Column(db.Boolean, default=False)
    
    # AI-generated adaptations (stored as JSON)
    simplified_versions = db.Column(db.Text)  # JSON: {level: text}
    summaries = db.Column(db.Text)  # JSON: {length: text}
    key_concepts = db.Column(db.Text)  # JSON list
    alt_text_descriptions = db.Column(db.Text)  # JSON for images
    tactile_diagrams = db.Column(db.Text)  # JSON for tactile representations
    
    # Relationships
    tags = db.relationship('ContentTag', backref='content', lazy='dynamic')
    interactions = db.relationship('UserInteraction', backref='content', lazy='dynamic')
    assessments = db.relationship('Assessment', backref='content', lazy='dynamic')
    
    def __repr__(self):
        return f'<Content {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content_type': self.content_type,
            'subject': self.subject,
            'topic': self.topic,
            'difficulty': self.difficulty,
            'body': self.body,
            'metadata': {
                'created_by': self.created_by,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None,
                'version': self.version,
                'language': self.language
            },
            'accessibility': {
                'has_alt_text': self.has_alt_text,
                'has_captions': self.has_captions,
                'has_transcript': self.has_transcript,
                'has_audio_description': self.has_audio_description
            },
            'ai_adaptations': {
                'simplified_versions': json.loads(self.simplified_versions) if self.simplified_versions else {},
                'summaries': json.loads(self.summaries) if self.summaries else {},
                'key_concepts': json.loads(self.key_concepts) if self.key_concepts else [],
                'alt_text_descriptions': json.loads(self.alt_text_descriptions) if self.alt_text_descriptions else {}
            }
        }
    
    def add_simplified_version(self, level, text):
        """Add a simplified version of the content"""
        versions = json.loads(self.simplified_versions) if self.simplified_versions else {}
        versions[level] = text
        self.simplified_versions = json.dumps(versions)
        db.session.commit()
    
    def get_simplified_version(self, level='intermediate'):
        """Get simplified version if available"""
        if self.simplified_versions:
            versions = json.loads(self.simplified_versions)
            return versions.get(level)
        return None

class ContentTag(db.Model):
    """Tags for categorizing content"""
    __tablename__ = 'content_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('content_id', 'tag'),)
    
    def __repr__(self):
        return f'<ContentTag {self.tag}>'

class Assessment(db.Model):
    """Assessments and quizzes"""
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    assessment_type = db.Column(db.String(50), default='quiz')  # quiz, test, assignment, project
    questions = db.Column(db.Text)  # JSON array of questions
    answers = db.Column(db.Text)  # JSON with correct answers
    max_score = db.Column(db.Integer, default=100)
    time_limit = db.Column(db.Integer)  # minutes, None for no limit
    allowed_attempts = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Assessment {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'content_id': self.content_id,
            'title': self.title,
            'assessment_type': self.assessment_type,
            'questions': json.loads(self.questions) if self.questions else [],
            'max_score': self.max_score,
            'time_limit': self.time_limit,
            'allowed_attempts': self.allowed_attempts
        }

class UserInteraction(db.Model):
    """Tracks user interactions with content"""
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    interaction_type = db.Column(db.String(50), nullable=False)  # view, complete, like, share, comment
    duration = db.Column(db.Integer)  # seconds
    engagement_score = db.Column(db.Float)  # 0.0 to 1.0
    comprehension_score = db.Column(db.Float)  # 0.0 to 1.0
    difficulty_rating = db.Column(db.Integer)  # 1-5
    accessibility_rating = db.Column(db.Integer)  # 1-5
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.Index('idx_user_content', 'user_id', 'content_id'),)
    
    def __repr__(self):
        return f'<UserInteraction user:{self.user_id} content:{self.content_id}>'