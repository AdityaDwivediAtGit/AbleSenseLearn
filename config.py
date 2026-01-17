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
    
    # Dev/Test Settings
    ENABLE_TEST_DATA = os.getenv('ENABLE_TEST_DATA', 'False').lower() == 'true'
    
    # AI Provider Settings
    AI_PROVIDER = "DeepSeek" # Default
    AI_BASE_URL = "https://genailab.tcs.in"
    AI_MODEL_NAME = "azure_ai/genailab-maas-DeepSeek-V3-0324"
    AI_SSL_VERIFY = False # Disable SSL verify for internal proxy
    
    # Validation
    if AI_PROVIDER == "DeepSeek" and not OPENAI_API_KEY:
        # We might want to warn or handle this, but for now just let it be.
        pass

    
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