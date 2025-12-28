import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ablesense.db')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # AI Settings
    VOICE_RATE = 150
    VOICE_VOLUME = 1.0
    
    # Directories to ensure exist
    DIRS_TO_CREATE = [
        os.path.join(DATA_DIR, 'user_profiles'),
        os.path.join(DATA_DIR, 'images'),
        os.path.join(STATIC_DIR, 'sounds'),
    ]

    @staticmethod
    def init_app():
        for d in Config.DIRS_TO_CREATE:
            os.makedirs(d, exist_ok=True)