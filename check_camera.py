import cv2
import time

def check_camera():
    print("Checking camera access...")
    
    # Try to open the camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Could not open camera! Please check your camera connection and permissions.")
        return False
    
    # Try to read a frame
    ret, frame = cap.read()
    
    if not ret:
        print("ERROR: Could not read from camera! Camera might be in use by another application.")
        cap.release()
        return False
    
    # Success!
    print("SUCCESS: Camera is working properly!")
    print(f"Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
    
    # Display the frame
    print("Showing camera feed for 5 seconds...")
    window_name = "Camera Test"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, frame)
    
    # Keep capturing frames for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if ret:
            cv2.imshow(window_name, frame)
        
        # Break loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    return True

if __name__ == "__main__":
    check_camera()
    print("\nIf your camera is working but the drowsiness detection server still has issues:")
    print("1. Make sure no other application is using the camera")
    print("2. Try restarting your computer")
    print("3. Check your browser's camera permissions")
    print("4. Make sure you've installed all required dependencies with 'pip install -r requirements.txt'") 