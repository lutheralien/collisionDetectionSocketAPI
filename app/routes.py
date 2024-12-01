from flask import Blueprint, jsonify, render_template
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """Render the main page"""
    logger.debug('Serving index page')
    return render_template('index.html')

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    logger.debug('Health check requested')
    return jsonify({
        "status": "healthy",
        "message": "Server is running"
    }), 200

# Optional: Status endpoint for the video processor
@main_bp.route('/status', methods=['GET'])
def stream_status():
    """Get the current status of video streaming"""
    from socket_server import video_processor  # Import here to avoid circular import
    
    status = video_processor.get_status()
    return jsonify(status), 200