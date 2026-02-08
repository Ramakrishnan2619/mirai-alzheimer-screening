"""Routes package."""
from .auth import auth_bp
from .predict import predict_bp
from .results import results_bp

__all__ = ['auth_bp', 'predict_bp', 'results_bp']
