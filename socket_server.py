from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS
from app.services.video_processor import VideoProcessor
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:4200"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Initialize SocketIO with proper CORS settings
socketio = SocketIO(
    app,
    cors_allowed_origins=["http://localhost:4200"],
    async_mode='threading',
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25
)

# Initialize video processor
video_processor = VideoProcessor(socketio)

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    join_room(client_id)
    logger.info(f'Client connected: {client_id}')
    socketio.emit('connection_status', 
                 {'status': 'connected', 'client_id': client_id}, 
                 room=client_id)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    logger.info(f'Client disconnected: {client_id}')
    video_processor.stop_processing(client_id)
    leave_room(client_id)

@socketio.on('start_stream')
def handle_start_stream():
    client_id = request.sid
    try:
        logger.info(f'Starting video stream for client: {client_id}')
        video_processor.start_processing(client_id, source=0)
        socketio.emit('stream_status', 
                     {'status': 'started'}, 
                     room=client_id)
    except Exception as e:
        logger.error(f'Error starting stream for client {client_id}: {str(e)}')
        socketio.emit('stream_error', 
                     {'error': str(e)}, 
                     room=client_id)

@socketio.on('stop_stream')
def handle_stop_stream():
    client_id = request.sid
    logger.info(f'Stopping video stream for client: {client_id}')
    video_processor.stop_processing(client_id)
    socketio.emit('stream_status', 
                 {'status': 'stopped'}, 
                 room=client_id)

@socketio.on_error()
def error_handler(e):
    client_id = request.sid
    logger.error(f'SocketIO error for client {client_id}: {str(e)}')
    socketio.emit('stream_error', 
                 {'error': str(e)}, 
                 room=client_id)

if __name__ == '__main__':
    logger.info('Starting SocketIO server...')
    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=5001,
            debug=True,
            allow_unsafe_werkzeug=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f'Failed to start server: {str(e)}')