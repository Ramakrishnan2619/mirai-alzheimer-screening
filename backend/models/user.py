"""
User Model
SQLAlchemy model for user authentication and profile data.
"""
from datetime import datetime
from backend.extensions import db, bcrypt


class User(db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to assessments
    assessments = db.relationship('Assessment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, email, password, full_name=None):
        self.email = email.lower().strip()
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.full_name = full_name
    
    def check_password(self, password):
        """Verify password against stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Serialize user to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
