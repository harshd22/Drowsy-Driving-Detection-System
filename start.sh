#!/bin/bash

# Print colorful messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========== SLOW ROADS WITH DROWSINESS DETECTION ==========${NC}"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 is not installed. Please install Python 3.6 or higher.${NC}"
    exit 1
fi

# Check if requirements are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
if ! python3 -c "import cv2, numpy, flask, flask_cors" &> /dev/null; then
    echo -e "${RED}Some dependencies are missing. Installing requirements...${NC}"
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install dependencies. Please install them manually:${NC}"
        echo "pip install -r requirements.txt"
        exit 1
    fi
fi

# Run camera check first
echo -e "${YELLOW}Checking camera...${NC}"
python3 check_camera.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Camera check failed. Continuing anyway, but drowsiness detection may not work.${NC}"
    read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
fi

# Start Drowsiness Detection Server
echo -e "${YELLOW}Starting Drowsiness Detection Server...${NC}"
python3 drowsy_detection_server.py &
FLASK_PID=$!

# Wait a moment for Flask to start
echo "Waiting for Flask server to start..."
sleep 3

# Check if Flask is running
if ! ps -p $FLASK_PID > /dev/null; then
    echo -e "${RED}ERROR: Flask server failed to start.${NC}"
    exit 1
fi

# Start HTTP Server
echo -e "${YELLOW}Starting Web Server on port 8000...${NC}"
python3 -m http.server 8000 &
HTTP_PID=$!

# Check if HTTP server is running
sleep 2
if ! ps -p $HTTP_PID > /dev/null; then
    echo -e "${RED}ERROR: HTTP server failed to start.${NC}"
    kill $FLASK_PID
    exit 1
fi

echo -e "${GREEN}Both servers are running!${NC}"
echo -e "${GREEN}Open your browser and navigate to: http://localhost:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"

# Trap SIGINT to kill both processes when user presses Ctrl+C
trap "echo -e '${YELLOW}Shutting down servers...${NC}'; kill $FLASK_PID $HTTP_PID; exit" INT

# Wait for both processes
wait 