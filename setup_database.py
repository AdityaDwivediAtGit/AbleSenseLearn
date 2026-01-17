from sqlalchemy import create_engine
from models.user import Base, User
from config import Config
import os

def init_db():
    Config.init_app()
    
    db_url = Config.DATABASE_URL
    print(f"Initializing database at {db_url}...")
    
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully.")
    
    # Verify if we should add a sample user
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if session.query(User).count() == 0:
        print("Creating sample users...")
        users = [
            User(
                username="demo_user",
                disability_type="visual",
                severity="moderate",
                font_size=20,
                voice_enabled=True,
                medical_info="Diabetic. Allergic to penicillin."
            ),
            User(
                username="alice_visual",
                disability_type="visual",
                severity="severe",
                font_size=24,
                voice_enabled=True,
                medical_info="None"
            ),
            User(
                username="bob_audio",
                disability_type="auditory",
                severity="severe",
                font_size=16,
                voice_enabled=False,
                medical_info="Uses hearing aid."
            ),
            User(
                username="charlie_cognitive",
                disability_type="cognitive",
                severity="moderate",
                font_size=18,
                voice_enabled=True,
                medical_info="Easily distracted."
            ),
            User(
                username="david_motor",
                disability_type="motor",
                severity="severe",
                font_size=16,
                voice_enabled=True,
                medical_info="Uses eye-tracking software."
            )
        ]
        session.add_all(users)
        session.commit()
        print("Sample users created: demo_user, alice_visual, bob_audio, charlie_cognitive, david_motor.")
    
    session.close()

if __name__ == "__main__":
    init_db()