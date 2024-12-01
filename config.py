import os

class Config:
    # Base configuration
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, 'app', 'models')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'uploads')
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SERVER_NAME = None  # Allow all hosts in development

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SERVER_NAME = None  # Configure for production

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}