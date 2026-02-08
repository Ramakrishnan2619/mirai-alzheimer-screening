"""
Flask Extensions
Central extension initialization for the MirAI application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS()


def init_extensions(app):
    """Initialize all Flask extensions with the app."""
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})
    
    # Create database tables
    with app.app_context():
        db.create_all()
