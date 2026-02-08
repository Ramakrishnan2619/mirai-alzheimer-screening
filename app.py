"""
MirAI Flask Application
Production-ready multi-stage Alzheimer's early-screening platform.
"""
import os
from flask import Flask, send_from_directory, jsonify
from config import config
from backend.extensions import init_extensions
from backend.routes import auth_bp, predict_bp, results_bp
from backend.services.model_loader import model_loader


def create_app(config_name=None):
    """Application factory."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    init_extensions(app)
    
    # Load ML models
    with app.app_context():
        try:
            model_loader.load_all()
        except Exception as e:
            print(f"⚠️ Warning: Could not load ML models: {e}")
            print("  API will use mock predictions until models are available.")
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(results_bp)
    
    # Serve frontend pages
    @app.route('/')
    def index():
        return send_from_directory('templates', 'index.html')
    
    @app.route('/register.html')
    def register_page():
        return send_from_directory('templates', 'register.html')
    
    @app.route('/login.html')
    def login_page():
        return send_from_directory('templates', 'login.html')
    
    @app.route('/assessment.html')
    def assessment_page():
        return send_from_directory('templates', 'assessment.html')
    
    @app.route('/results.html')
    def results_page():
        return send_from_directory('templates', 'results.html')
    
    # Serve static assets
    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)
    
    @app.route('/assets/<path:path>')
    def serve_assets(path):
        return send_from_directory('static/assets', path)
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'models_loaded': model_loader.is_loaded(),
            'version': '2.0.0'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
