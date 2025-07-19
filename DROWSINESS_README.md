# Drowsiness Detection for Slow Roads

This extension adds a drowsiness detection system to Slow Roads. When the system detects that the player is drowsy (eyes closed for an extended period), it automatically switches the vehicle to self-driving mode.

## Features

- Real-time drowsiness detection using your webcam
- Automatic switching to self-driving mode when drowsiness is detected
- Visual feedback showing your webcam feed and drowsiness status
- Manual toggle for self-driving mode (press 'D' key or use the button)

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- Web browser with webcam access
- The required Python packages (install using `pip install -r requirements.txt`):
  - OpenCV
  - NumPy
  - Flask
  - Flask-CORS

### Getting Started

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Start the drowsiness detection server:
   ```
   python drowsy_detection_server.py
   ```

3. Start the web server to run Slow Roads:
   ```
   python -m http.server 8000
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

5. Allow webcam access when prompted by your browser

## How It Works

1. The drowsiness detection server uses OpenCV and Haar cascades to detect faces and eyes in the webcam feed
2. When the system detects closed eyes for a certain number of consecutive frames, it triggers drowsiness detection
3. When drowsiness is detected, the JavaScript client automatically switches the game to self-driving mode
4. The self-driving mode keeps the car moving forward at a steady pace
5. When the driver is alert again (eyes open), they can manually take control by clicking the toggle button

## Troubleshooting

- If the webcam feed doesn't appear, make sure you've allowed camera access in your browser
- If the detection server doesn't start, check that you have all the required Python packages installed
- If self-driving doesn't activate, check the browser console for any error messages

## Privacy Note

The webcam feed is processed locally on your machine and is not sent to any external servers.

## Credits

- Original Slow Roads game by Anslo
- Drowsiness detection system implemented using OpenCV and Python 