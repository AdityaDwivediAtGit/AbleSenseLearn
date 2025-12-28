from datetime import datetime
from app import db
import json

class LearningPathway(db.Model):
    """Personalized learning pathways"""
    __tablename__ = 'learning_pathways'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(100))
    goal = db.Column(db.Text)
    estimated_completion_time = db.Column(db.Integer)  # hours
    current_progress = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    
    # Pathway structure (JSON)
    structure = db.Column(db.Text)  # JSON array of pathway items
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<LearningPathway {self.title} for user:{self.user_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'goal': self.goal,
            'estimated_completion_time': self.estimated_completion_time,
            'current_progress': self.current_progress,
            'structure': json.loads(self.structure) if self.structure else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def update_progress(self):
        """Update progress based on completed items"""
        structure = json.loads(self.structure) if self.structure else []
        if not structure:
            self.current_progress = 0.0
            return
        
        completed_items = sum(1 for item in structure if item.get('completed', False))
        total_items = len(structure)
        self.current_progress = completed_items / total_items
        db.session.commit()

class PathwayItem(db.Model):
    """Individual items in a learning pathway"""
    __tablename__ = 'pathway_items'
    
    id = db.Column(db.Integer, primary_key=True)
    pathway_id = db.Column(db.Integer, db.ForeignKey('learning_pathways.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    item_type = db.Column(db.String(50), nullable=False)  # content, assessment, activity, break
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    estimated_duration = db.Column(db.Integer)  # minutes
    prerequisites = db.Column(db.Text)  # JSON array of item IDs
    
    # Completion tracking
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Float)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('pathway_id', 'order'),
        db.Index('idx_pathway_order', 'pathway_id', 'order'),
    )
    
    def __repr__(self):
        return f'<PathwayItem {self.title} in pathway:{self.pathway_id}>'
    
    def mark_completed(self, score=None, notes=None):
        """Mark item as completed"""
        self.completed_at = datetime.utcnow()
        if score is not None:
            self.score = score
        if notes:
            self.notes = notes
        db.session.commit()

class ProgressTracker(db.Model):
    """Tracks overall learning progress"""
    __tablename__ = 'progress_tracker'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    
    # Daily metrics
    total_study_time = db.Column(db.Integer, default=0)  # minutes
    completed_items = db.Column(db.Integer, default=0)
    average_engagement = db.Column(db.Float, default=0.0)
    average_comprehension = db.Column(db.Float, default=0.0)
    
    # Subject-specific progress (stored as JSON)
    subject_progress = db.Column(db.Text)  # JSON: {subject: {score, items_completed}}
    
    # Goals
    daily_goal_met = db.Column(db.Boolean, default=False)
    weekly_goal_met = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'date'),)
    
    def __repr__(self):
        return f'<ProgressTracker user:{self.user_id} date:{self.date}>'
    
    def update_subject_progress(self, subject, score_delta, items_completed=1):
        """Update progress for a specific subject"""
        progress = json.loads(self.subject_progress) if self.subject_progress else {}
        
        if subject not in progress:
            progress[subject] = {'total_score': 0, 'items_completed': 0, 'average_score': 0}
        
        subject_data = progress[subject]
        subject_data['total_score'] += score_delta
        subject_data['items_completed'] += items_completed
        subject_data['average_score'] = subject_data['total_score'] / subject_data['items_completed']
        
        self.subject_progress = json.dumps(progress)
        db.session.commit()

class LearningGoal(db.Model):
    """User learning goals"""
    __tablename__ = 'learning_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    goal_type = db.Column(db.String(50))  # daily, weekly, monthly, long_term
    target_date = db.Column(db.Date)
    target_value = db.Column(db.Float)  # e.g., 90% score, 5 items completed
    current_value = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(50))  # percent, items, minutes, score
    
    # Categories
    subject = db.Column(db.String(100))
    skill = db.Column(db.String(100))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<LearningGoal {self.title} for user:{self.user_id}>'
    
    def update_progress(self, new_value):
        """Update goal progress"""
        self.current_value = new_value
        if self.target_value and self.current_value >= self.target_value:
            self.completed_at = datetime.utcnow()
            self.is_active = False
        db.session.commit()
    
    def get_progress_percentage(self):
        """Get progress as percentage"""
        if not self.target_value:
            return 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)