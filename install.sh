#!/bin/bash

# Installation script for the Clinic Queue Management System on Raspberry Pi OS

# Ensure the script is run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo: sudo ./install.sh"
  exit
fi

echo "--- Starting Installation ---"

# --- Step 1: Update package list and install system dependencies ---
echo ">>> [1/4] Updating package list and installing system dependencies..."
apt-get update
apt-get install -y python3-venv python3-pip mpg123 mosquitto mosquitto-clients

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
# This part should be run as the regular user, not root.
# We create the directory and set permissions.
echo ">>> [2/4] Creating Python virtual environment..."
# We assume the script is run from the project directory.
PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"

# Find a non-root user to own the venv directory
# If the script is run with sudo, SUDO_USER is the original user.
REGULAR_USER=$SUDO_USER
if [ -z "$REGULAR_USER" ]; then
    # Fallback if SUDO_USER is not set
    REGULAR_USER=$(ls /home | head -n 1)
    echo "Warning: Could not determine the original user. Using '$REGULAR_USER' as the owner of the venv."
fi

# Create venv as the regular user
sudo -u "$REGULAR_USER" python3 -m venv "$VENV_DIR"
echo "Virtual environment created at $VENV_DIR"
echo ""

# --- Step 3: Install Python packages ---
echo ">>> [3/4] Installing Python packages..."
# Activate venv and install packages
# The packages must be installed for the venv's Python interpreter
"$VENV_DIR/bin/pip" install PyQt5 Flask Flask-Cors paho-mqtt Pillow
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

