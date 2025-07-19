import cv2
import numpy as np
import math
import time
from flask import Flask, Response, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
# Update CORS configuration to explicitly allow requests from localhost:8000
CORS(app, resources={r"/*": {"origins": ["http://localhost:8000", "http://127.0.0.1:8000"]}})

# Global variable to store drowsiness state
is_drowsy = False

class SleepDetection:
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Initialize face and eye detectors
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Constants
        self.EYE_CLOSED_THRESHOLD = 10  # Frames to trigger drowsiness alert
        
        # State variables
        self.closed_eyes_counter = 0
        
    def detect_eyes(self, frame):
        global is_drowsy
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        
        if len(faces) == 0:
            return "no_face", frame
        
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        eyes = self.eye_cascade.detectMultiScale(face_roi, 1.1, 3)
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        if len(eyes) < 2:
            return "eyes_closed", frame
        else:
            return "eyes_open", frame
    
    def run(self):
        global is_drowsy
        print("Starting Sleep Detection System...")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Detect eyes
            status, frame = self.detect_eyes(frame)
            
            # Update drowsiness state
            if status == "eyes_closed":
                self.closed_eyes_counter += 1
                if self.closed_eyes_counter >= self.EYE_CLOSED_THRESHOLD:
                    is_drowsy = True
            else:
                self.closed_eyes_counter = 0
                is_drowsy = False
            
            # Display status on main frame
            status_text = "DROWSY DETECTED" if is_drowsy else "ALERT"
            text_color = (0, 0, 255) if is_drowsy else (0, 255, 0)
            cv2.putText(frame, status_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
            
            # Convert frame to JPEG for streaming
            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            
            # Yield the frame as part of a multipart response
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Small delay to reduce CPU usage
            time.sleep(0.03)

# Initialize the sleep detection
detector = SleepDetection()

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    # Add CORS headers specifically for this endpoint
    response = Response(
        detector.run(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/drowsy_status')
def drowsy_status():
    """Return current drowsiness status as JSON."""
    global is_drowsy
    response = jsonify({"is_drowsy": is_drowsy})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == "__main__":
    # Start the Flask app
    run_flask() 