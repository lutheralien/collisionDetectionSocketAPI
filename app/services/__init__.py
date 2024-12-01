from flask import Flask
from flask_cors import CORS
from config import config
import os

def create_app(config_name=None):
    # Get configuration name from environment or use default
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:4200"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # Initialize models folder
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    return app