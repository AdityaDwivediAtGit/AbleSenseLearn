import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ablelearn.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Model configurations
    HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN', '')
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
    
    # Content settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'docx'}
    
    # Accessibility settings
    DEFAULT_FONT_SIZE = 16
    DEFAULT_THEME = 'light'
    
    # Learning settings
    DEFAULT_SIMPLIFICATION_LEVEL = 'intermediate'
    ENABLE_VOICE_COMMANDS = True
    
    # Paths
    UPLOAD_FOLDER = 'static/uploads'
    MODEL_CACHE_DIR = 'data/ml_models'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['MODEL_CACHE_DIR'], exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Production-specific initialization
        # Add security headers, logging, etc.

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}