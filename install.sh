#!/bin/bash

# Installation script for the Clinic Queue Management System on Raspberry Pi OS
# This script uses system packages for PyQt5 and sets up a systemd service for auto-start.

# Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo: sudo ./install.sh"
  exit
fi

echo "--- Starting Installation ---"

# --- Step 1: Update package list and install system dependencies ---
echo ">>> [1/5] Updating package list and installing system dependencies..."
apt-get update
# Install core tools, audio player, MQTT broker, and Qt dependencies for PyQt5
apt-get install -y python3-venv python3-pip mpg123 mosquitto mosquitto-clients qtbase5-dev python3-pyqt5

# Check if mosquitto is active
systemctl is-active --quiet mosquitto
if [ $? -eq 0 ]; then
    echo "Mosquitto MQTT broker is installed and active."
else
    echo "Warning: Mosquitto MQTT broker was installed but is not running. You may need to enable it with 'sudo systemctl enable --now mosquitto'"
fi
echo ">>> System dependencies installed."
echo ""

# --- Step 2: Create a Python virtual environment ---
echo ">>> [2/5] Creating Python virtual environment..."
PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"

if [ -d "$VENV_DIR" ]; then
    echo "Removing old virtual environment."
    rm -rf "$VENV_DIR"
fi

REGULAR_USER=$SUDO_USER
if [ -z "$REGULAR_USER" ]; then
    REGULAR_USER=$(ls /home | head -n 1)
    echo "Warning: Could not determine the original user. Using '$REGULAR_USER' as the owner of the venv."
fi

echo "Creating venv with access to system site-packages (for PyQt5)."
sudo -u "$REGULAR_USER" python3 -m venv --system-site-packages "$VENV_DIR"
echo "Virtual environment created at $VENV_DIR"
echo ""

# --- Step 3: Install Python packages ---
echo ">>> [3/5] Installing remaining Python packages via pip..."
"$VENV_DIR/bin/pip" install Flask Flask-Cors paho-mqtt Pillow gTTS
echo ">>> Python packages installed."
echo ""

# --- Step 4: Generate audio assets (gTTS, uses Internet) ---
echo ">>> [4/6] Generating audio assets (requires Internet access for gTTS)..."
sudo -u "$REGULAR_USER" mkdir -p "$PROJECT_DIR/output"
sudo -u "$REGULAR_USER" "$VENV_DIR/bin/python" "$PROJECT_DIR/output/gen.py"
echo ">>> Audio assets generated in $PROJECT_DIR/output."
echo ""

# --- Step 5: Setup systemd service ---
echo ">>> [5/6] Setting up systemd service for auto-start..."
if [ -f "inline.service" ]; then
    # Copy the service file to the systemd directory
    cp inline.service /etc/systemd/system/inline.service
    # Reload the systemd daemon to recognize the new service
    systemctl daemon-reload
    # Enable the service to start on boot
    systemctl enable inline.service
    echo ">>> Service 'inline.service' created and enabled."
else
    echo ">>> WARNING: 'inline.service' file not found. Skipping systemd setup."
fi
echo ""

# --- Step 6: Final instructions ---
echo ">>> [6/6] Installation Complete!"
echo ""
echo "--- Next Steps ---"
echo "1. Configure Zigbee buttons as described in README.md"
echo ""
echo "2. REBOOT the Raspberry Pi for all changes to take effect."
echo "   sudo reboot"
echo ""
echo "3. After rebooting, the application should start automatically."
echo ""
echo "4. You can manage the application using these commands:"
echo "   - Check status: sudo systemctl status inline"
echo "   - Stop the service: sudo systemctl stop inline"
echo "   - Start the service: sudo systemctl start inline"
echo "   - View logs: sudo journalctl -u inline -f"
echo ""
echo "--- Installation Finished ---"
