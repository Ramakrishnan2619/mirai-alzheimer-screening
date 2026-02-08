"""
MirAI Configuration
Environment-driven configuration for Flask application.
"""
import os
from datetime import timedelta

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

# Ensure instance directory exists
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mirai-dev-secret-key-change-in-production')
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'mirai-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = False  # Set True in production with HTTPS
    JWT_COOKIE_CSRF_PROTECT = False
    
    # Database - use absolute path
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(INSTANCE_DIR, "mirai.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # ML Models Path
    ML_MODELS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend', 'ml_models')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    JWT_COOKIE_SECURE = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
