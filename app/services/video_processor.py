import cv2
import base64
import numpy as np
import threading
from datetime import datetime
from .object_detection import ObjectDetector
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, socketio):
        self.socketio = socketio
        self.detector = ObjectDetector()
        # Dictionary to store processing status for each client
        self.client_streams: Dict[str, dict] = {}
        self.lock = threading.Lock()

    def start_processing(self, client_id: str, source=0):
        """Start video processing for a specific client"""
        with self.lock:
            if client_id in self.client_streams:
                logger.warning(f"Client {client_id} already has an active stream")
                return

            # Initialize client stream
            self.client_streams[client_id] = {
                'is_processing': True,
                'thread': threading.Thread(
                    target=self._process_video,
                    args=(client_id, source)
                ),
                'source': source,
                'frame_count': 0
            }
            
            # Start processing thread
            self.client_streams[client_id]['thread'].daemon = True
            self.client_streams[client_id]['thread'].start()
            logger.info(f"Started stream for client {client_id}")

    def stop_processing(self, client_id: str):
        """Stop video processing for a specific client"""
        with self.lock:
            if client_id in self.client_streams:
                logger.info(f"Stopping stream for client {client_id}")
                self.client_streams[client_id]['is_processing'] = False
                self.client_streams[client_id]['thread'].join()
                del self.client_streams[client_id]
                logger.info(f"Stopped stream for client {client_id}")

    def _process_video(self, client_id: str, source):
        """Process video for a specific client"""
        cap = cv2.VideoCapture(source)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video source for client {client_id}")
            self.socketio.emit('stream_error', 
                             {'error': 'Failed to open video source'},
                             room=client_id)
            return

        try:
            while (client_id in self.client_streams and 
                   self.client_streams[client_id]['is_processing']):
                ret, frame = cap.read()
                
                if not ret:
                    if isinstance(source, str):  # Video file
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    else:
                        break

                try:
                    # Process frame with object detection
                    detections, collisions = self.detector.detect_vehicles(frame)
                    processed_frame = self.detector.draw_detections_and_collisions(
                        frame.copy(), detections, collisions)

                    # Convert to base64
                    _, buffer = cv2.imencode('.jpg', processed_frame)
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')

                    # Emit frame to specific client
                    self.socketio.emit('video_frame', {
                        'frame': frame_base64,
                        'detections': len(detections),
                        'collisions': len(collisions),
                        'timestamp': datetime.now().isoformat(),
                        'frame_number': self.client_streams[client_id]['frame_count']
                    }, room=client_id)

                    self.client_streams[client_id]['frame_count'] += 1
                    cv2.waitKey(1)

                except Exception as e:
                    logger.error(f"Error processing frame for client {client_id}: {str(e)}")
                    self.socketio.emit('stream_error', 
                                     {'error': str(e)},
                                     room=client_id)
                    continue

        except Exception as e:
            logger.error(f"Error in video processing for client {client_id}: {str(e)}")
            self.socketio.emit('stream_error', 
                             {'error': str(e)},
                             room=client_id)

        finally:
            cap.release()
            with self.lock:
                if client_id in self.client_streams:
                    self.client_streams[client_id]['is_processing'] = False
                    self.socketio.emit('stream_stopped', room=client_id)

    def get_client_status(self, client_id: str) -> dict:
        """Get status for a specific client"""
        with self.lock:
            if client_id in self.client_streams:
                return {
                    'is_processing': self.client_streams[client_id]['is_processing'],
                    'frame_count': self.client_streams[client_id]['frame_count'],
                    'source': self.client_streams[client_id]['source']
                }
            return {'is_processing': False, 'frame_count': 0, 'source': None}