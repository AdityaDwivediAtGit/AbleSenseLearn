from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Disability Profile
    disability_type = Column(String)  # 'visual', 'hearing', 'motor', 'cognitive', 'none'
    severity = Column(String)         # 'mild', 'moderate', 'severe'
    
    # Preferences
    font_size = Column(Integer, default=16)
    high_contrast = Column(Boolean, default=False)
    voice_enabled = Column(Boolean, default=True)
    voice_speed = Column(Integer, default=150)
    
    # Emergency Contact
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    medical_info = Column(Text, nullable=True)

    interactions = relationship("InteractionLog", back_populates="user")

class InteractionLog(Base):
    __tablename__ = 'interaction_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    interaction_type = Column(String) # 'voice_command', 'vision_request', 'chat'
    input_content = Column(Text)
    response_content = Column(Text)
    
    user = relationship("User", back_populates="interactions")