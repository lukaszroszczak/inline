# Clinic Queue Management System

A comprehensive patient queue management system designed for a medical clinic with multiple doctor's offices. The application displays the current patient number on a fullscreen display, provides audio announcements, and can be controlled via both physical Zigbee buttons and a web-based interface.

The user interface and logic are written in Polish.

---

## 🇵🇱 Opis po Polsku

System do zarządzania kolejką pacjentów w przychodni. Aplikacja wyświetla na pełnoekranowym monitorze aktualnie obsługiwane numerki dla trzech gabinetów. Sterowanie odbywa się za pomocą bezprzewodowych przycisków Zigbee (poprzez MQTT), a także przez panel webowy (Flask), który umożliwia zdalne zarządzanie kolejkami (dodawanie, usuwanie pacjentów, zmiana numeru). Po wezwaniu nowego pacjenta, system odtwarza komunikat głosowy z numerem pacjenta i numerem gabinetu.

---

## ✨ Features

*   **Fullscreen Display:** A clean, scalable fullscreen display showing the currently served number for up to three offices.
*   **Systemd Service:** Runs as a background service, starting automatically on boot and restarting on failure.
*   **Zigbee Button Control:** Doctors can call the next or previous patient using wireless Zigbee buttons.
*   **Web Control Panel:** A comprehensive web interface for remote management of queues and patient lists.
*   **Audio Announcements:** Announces the number and office when a new patient is called.
*   **Customizable UI:** The UI appearance can be customized via `gui.ini`.
*   **Multi-threaded Architecture:** The GUI, web server, and MQTT client run in separate threads for a responsive experience.

## ⚙️ Tech Stack

*   **Backend & GUI:** Python, PyQt5 (via system packages)
*   **Web Framework:** Flask
*   **Comms:** Paho-MQTT (for Zigbee2MQTT)
*   **Hardware:** Zigbee buttons, Zigbee coordinator
*   **Audio:** `mpg123`
*   **OS:** Debian-based Linux (e.g., Raspberry Pi OS)
*   **Service Management:** systemd

## 🚀 Getting Started on Raspberry Pi

This project is designed to be run on a Raspberry Pi connected to a display.

### 1. Installation

The installation process is automated with a script.

```bash
# Clone the repository
git clone https://github.com/lukaszroszczak/inline.git
cd inline

# Run the installation script with sudo
sudo ./install.sh
```
The script will:
*   Install all system dependencies (like `mpg123`, `mosquitto`, `python3-pyqt5`).
*   Set up a Python virtual environment.
*   Install required Python packages.
*   Set up and enable a `systemd` service to run the application automatically on boot.

### 2. Configuration

Before rebooting, you should configure the application:

*   **Zigbee Buttons:** Edit `main_program.py` and update the `button_id_to_column` dictionary with the IEEE addresses of your Zigbee buttons.
*   **UI (Optional):** Edit `gui.ini` to customize the UI appearance if needed.
*   **Audio Files:** Make sure you have all the required announcement sounds (e.g., `dingdong.mp3`, `101.mp3`, `gabinet_nr_1.mp3`) in the `output/` directory.

### 3. Reboot

After the installation and configuration are complete, reboot the Raspberry Pi.

```bash
sudo reboot
```

## ⚙️ Managing the Application

The application now runs as a `systemd` service named `inline`. It will start automatically after the reboot.

You can manage it using standard `systemctl` commands:

*   **Check the status:**
    ```bash
    sudo systemctl status inline
    ```

*   **View live logs:**
    ```bash
    sudo journalctl -u inline -f
    ```

*   **Stop the service:**
    ```bash
    sudo systemctl stop inline
    ```

*   **Start the service manually:**
    ```bash
    sudo systemctl start inline
    ```

*   **Disable auto-start on boot:**
    ```bash
    sudo systemctl disable inline
    ```