#!/bin/bash

# Installation script for the Clinic Queue Management System on Raspberry Pi OS
# This script uses system packages for PyQt5 for better stability and performance.

# Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo: sudo ./install.sh"
  exit
fi

echo "--- Starting Installation ---"

# --- Step 1: Update package list and install system dependencies ---
echo ">>> [1/4] Updating package list and installing system dependencies..."
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
echo ">>> [2/4] Creating Python virtual environment..."
# This part should be run as the regular user, not root.
# We create the directory and set permissions.
PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"

# Remove old venv if it exists
if [ -d "$VENV_DIR" ]; then
    echo "Removing old virtual environment."
    rm -rf "$VENV_DIR"
fi

# Find a non-root user to own the venv directory
# If the script is run with sudo, SUDO_USER is the original user.
REGULAR_USER=$SUDO_USER
if [ -z "$REGULAR_USER" ]; then
    # Fallback if SUDO_USER is not set
    REGULAR_USER=$(ls /home | head -n 1)
    echo "Warning: Could not determine the original user. Using '$REGULAR_USER' as the owner of the venv."
fi

# Create venv with --system-site-packages to inherit system's PyQt5
echo "Creating venv with access to system site-packages (for PyQt5)."
sudo -u "$REGULAR_USER" python3 -m venv --system-site-packages "$VENV_DIR"
echo "Virtual environment created at $VENV_DIR"
echo ""

# --- Step 3: Install Python packages ---
echo ">>> [3/4] Installing remaining Python packages via pip..."
# The packages must be installed for the venv's Python interpreter
# PyQt5 is already installed via apt, so we only need the others.
"$VENV_DIR/bin/pip" install Flask Flask-Cors paho-mqtt Pillow
echo ">>> Python packages installed."
echo ""

# --- Step 4: Final instructions ---
echo ">>> [4/4] Installation Complete!"
echo ""
echo "--- Next Steps ---"
echo "1. Activate the virtual environment in your terminal:"
echo "   source ${VENV_DIR}/bin/activate"
echo ""
echo "2. Configure the Zigbee buttons:"
echo "   - Make sure Zigbee2MQTT is running and your buttons are paired."
echo "   - Edit 'main_program.py' and update the 'button_id_to_column' dictionary with your button IDs."
echo ""
echo "3. Generate Audio Files:"
echo "   - Make sure you have all the required announcement sounds (e.g., 'dingdong.mp3', '101.mp3', 'gabinet_nr_1.mp3') in the 'output/' directory."
echo ""
echo "4. Run the application:"
echo "   (After activating the venv)"
echo "   python3 main_program.py"
echo ""
echo "--- Installation Finished ---"