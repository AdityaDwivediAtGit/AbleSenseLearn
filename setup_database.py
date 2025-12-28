#!/usr/bin/env python3
"""Database setup script"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Content, LearningProfile, AccessibilityProfile
import json

def setup_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Create sample users
        print("Creating sample users...")
        
        # Sample teacher
        teacher = User(
            username='teacher1',
            email='teacher@school.edu',
            role='teacher',
            full_name='Jane Smith'
        )
        teacher.set_password('teacher123')
        db.session.add(teacher)
        
        # Sample student with dyslexia profile
        student1 = User(
            username='student_dyslexia',
            email='student1@school.edu',
            role='student',
            full_name='Alex Johnson'
        )
        student1.set_password('student123')
        db.session.add(student1)
        
        # Sample student with visual impairment
        student2 = User(
            username='student_visual',
            email='student2@school.edu',
            role='student',
            full_name='Maria Garcia'
        )
        student2.set_password('student123')
        db.session.add(student2)
        
        db.session.commit()
        
        # Create accessibility profiles
        print("Creating accessibility profiles...")
        
        # Dyslexia profile
        dyslexia_profile = AccessibilityProfile(
            user_id=student1.id,
            disability_type='dyslexia',
            preferred_font='OpenDyslexic',
            preferred_font_size=18,
            line_spacing=1.5,
            high_contrast_mode=False,
            requires_simplified_text=True,
            simplification_level='advanced',
            text_to_speech_enabled=True,
            speech_rate=0.8
        )
        db.session.add(dyslexia_profile)
        
        # Visual impairment profile
        visual_profile = AccessibilityProfile(
            user_id=student2.id,
            disability_type='low_vision',
            preferred_font='Arial',
            preferred_font_size=24,
            line_spacing=2.0,
            high_contrast_mode=True,
            requires_simplified_text=False,
            simplification_level='basic',
            text_to_speech_enabled=True,
            speech_rate=1.0,
            screen_reader_enabled=True
        )
        db.session.add(visual_profile)
        
        # Create sample content
        print("Creating sample content...")
        
        sample_content = [
            Content(
                title='Introduction to Photosynthesis',
                content_type='lesson',
                subject='Biology',
                difficulty='intermediate',
                body="""
                Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water. Photosynthesis in plants generally involves the green pigment chlorophyll and generates oxygen as a byproduct.

                The overall chemical reaction of photosynthesis is:
                6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂

                This means that six molecules of carbon dioxide react with six molecules of water in the presence of sunlight to produce one molecule of glucose and six molecules of oxygen.

                Photosynthesis occurs in two main stages:
                1. Light-dependent reactions
                2. Light-independent reactions (Calvin Cycle)
                """,
                created_by=teacher.id
            ),
            Content(
                title='Basic Algebra: Solving Equations',
                content_type='lesson',
                subject='Mathematics',
                difficulty='beginner',
                body="""
                An equation is a mathematical statement that asserts the equality of two expressions. Solving an equation means finding the value(s) of the variable(s) that make the equation true.

                For example, to solve the equation: 2x + 3 = 11

                Steps:
                1. Subtract 3 from both sides: 2x = 8
                2. Divide both sides by 2: x = 4

                Let's verify: 2(4) + 3 = 8 + 3 = 11 ✓

                Remember: Whatever you do to one side of the equation, you must do to the other side to maintain balance.
                """,
                created_by=teacher.id
            )
        ]
        
        for content in sample_content:
            db.session.add(content)
        
        db.session.commit()
        
        # Create learning profiles
        print("Creating learning profiles...")
        
        learning_profile1 = LearningProfile(
            user_id=student1.id,
            learning_style='visual',
            pace='moderate',
            preferred_modality='text+audio',
            strengths=['pattern_recognition', 'creativity'],
            challenges=['reading_fluency', 'spelling'],
            accommodations=['extra_time', 'text_to_speech']
        )
        db.session.add(learning_profile1)
        
        learning_profile2 = LearningProfile(
            user_id=student2.id,
            learning_style='auditory',
            pace='slow',
            preferred_modality='audio',
            strengths=['listening_comprehension', 'verbal_expression'],
            challenges=['visual_processing', 'reading_small_text'],
            accommodations=['screen_reader', 'high_contrast']
        )
        db.session.add(learning_profile2)
        
        db.session.commit()
        
        print("Database setup complete!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Content.query.count()} content items")
        print(f"Created {AccessibilityProfile.query.count()} accessibility profiles")

if __name__ == '__main__':
    setup_database()