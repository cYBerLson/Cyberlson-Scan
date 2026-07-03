import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class for SecureCheck-NG."""
    
    # Flask Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-local-only-replace-in-prod')
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    
    # Session Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security Headers (handled by Flask-Talisman but can be configured here)
    STRICT_TRANSPORT_SECURITY = True
    STRICT_TRANSPORT_SECURITY_PRELOAD = True
    STRICT_TRANSPORT_SECURITY_MAX_AGE = 31536000  # 1 year
    
    # App Specific
    APP_NAME = "Cyberlson Scan"
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # In production, ensure SECRET_KEY is set in environment
    @classmethod
    def init_app(cls, app):
        if cls.SECRET_KEY == 'dev-key-for-local-only-replace-in-prod':
            app.logger.warning("SECRET_KEY is using the default development value!")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP for local dev

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
