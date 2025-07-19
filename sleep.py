import cv2
import numpy as np
import math

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
        self.EYE_CLOSED_THRESHOLD = 10  # Frames to trigger wheel stop
        self.WHEEL_SPEED = 5  # Degrees per frame
        
        # State variables
        self.closed_eyes_counter = 0
        self.wheel_angle = 0
        self.wheel_running = True
        
        # Create windows
        cv2.namedWindow('Sleep Detection')
        cv2.namedWindow('Wheel Simulation')
    
    def detect_eyes(self, frame):
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
    
    def draw_wheel(self, frame, center, radius, angle, status):
        # Draw wheel rim
        cv2.circle(frame, center, radius, (200, 200, 200), 8)
        
        # Draw center hub
        cv2.circle(frame, center, radius//6, (100, 100, 100), -1)
        
        # Draw spokes
        num_spokes = 6
        for i in range(num_spokes):
            spoke_angle = angle + i * (360 / num_spokes)
            rad = math.radians(spoke_angle)
            x1 = int(center[0] + (radius//6) * math.cos(rad))
            y1 = int(center[1] + (radius//6) * math.sin(rad))
            x2 = int(center[0] + radius * math.cos(rad))
            y2 = int(center[1] + radius * math.sin(rad))
            cv2.line(frame, (x1, y1), (x2, y2), (50, 50, 50), 5)
        
        # Add status text
        text = "RUNNING" if status else "STOPPED"
        color = (0, 255, 0) if status else (0, 0, 255)
        cv2.putText(frame, text, (center[0] - 50, center[1] + radius + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame
    
    def run(self):
        print("Starting Sleep Detection System...")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Detect eyes
            status, frame = self.detect_eyes(frame)
            
            # Update wheel status
            if status == "eyes_closed":
                self.closed_eyes_counter += 1
                if self.closed_eyes_counter >= self.EYE_CLOSED_THRESHOLD:
                    self.wheel_running = False
            else:
                if self.closed_eyes_counter > 0:
                    self.closed_eyes_counter = max(0, self.closed_eyes_counter - 1)
                if self.closed_eyes_counter == 0:
                    self.wheel_running = True
            
            # Update wheel angle
            if self.wheel_running:
                self.wheel_angle = (self.wheel_angle + self.WHEEL_SPEED) % 360
            
            # Create wheel simulation frame
            wheel_frame = np.zeros((400, 400, 3), dtype=np.uint8)
            wheel_center = (200, 200)
            wheel_radius = 150
            wheel_frame = self.draw_wheel(wheel_frame, wheel_center, wheel_radius, 
                                        self.wheel_angle, self.wheel_running)
            
            # Display status on main frame
            status_text = "EYES CLOSED" if status == "eyes_closed" else "EYES OPEN"
            text_color = (0, 0, 255) if status == "eyes_closed" else (0, 255, 0)
            cv2.putText(frame, status_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
            
            # Display frames
            cv2.imshow('Sleep Detection', frame)
            cv2.imshow('Wheel Simulation', wheel_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = SleepDetection()
    detector.run()