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
        print("Creating sample user...")
        sample_user = User(
            username="demo_user",
            disability_type="visual",
            severity="moderate",
            font_size=20,
            voice_enabled=True,
            medical_info="Diabetic. Allergic to penicillin."
        )
        session.add(sample_user)
        session.commit()
        print("Sample user 'demo_user' created.")
    
    session.close()

if __name__ == "__main__":
    init_db()