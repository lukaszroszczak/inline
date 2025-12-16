# Clinic Queue Management System

A comprehensive patient queue management system designed for a medical clinic with multiple doctor's offices. The application displays the current patient number on a fullscreen display, provides audio announcements, and can be controlled via both physical Zigbee buttons and a web-based interface.

The user interface and logic are written in Polish.

---

## 🇵🇱 Opis po Polsku

System do zarządzania kolejką pacjentów w przychodni. Aplikacja wyświetla na pełnoekranowym monitorze aktualnie obsługiwane numerki dla trzech gabinetów. Sterowanie odbywa się za pomocą bezprzewodowych przycisków Zigbee (poprzez MQTT), a także przez panel webowy (Flask), który umożliwia zdalne zarządzanie kolejkami (dodawanie, usuwanie pacjentów, zmiana numeru). Po wezwaniu nowego pacjenta, system odtwarza komunikat głosowy z numerem pacjenta i numerem gabinetu.

---

## ✨ Features

*   **Fullscreen Display:** A clean, scalable fullscreen display showing the currently served number for up to three offices. Built with PyQt5.
*   **Zigbee Button Control:** Doctors can call the next or previous patient using wireless Zigbee buttons.
    *   Communicates via an MQTT broker (e.g., Zigbee2MQTT).
    *   Supports single press, double press, and long press actions.
    *   Monitors button battery levels.
*   **Web Control Panel:** A comprehensive web interface built with Flask for remote management.
    *   View the status of all queues.
    *   Increment, decrement, or reset the number for any office.
    *   Manage the patient list for each office: add, remove, or edit patient entries and notes.
*   **Audio Announcements:** When a new number is called, a voice announces the number and the corresponding office (e.g., "Number 101, to office 1").
    *   Uses pre-generated MP3 files for announcements.
*   **Customizable UI:** The user interface appearance (colors, fonts, scaling) can be customized via a `gui.ini` configuration file.
*   **Multi-threaded Architecture:** The GUI, web server, and MQTT client run in separate threads for a responsive experience.

## ⚙️ Tech Stack

*   **Backend & GUI:** Python
    *   **PyQt5:** For the fullscreen graphical user interface.
    *   **Flask:** For the web-based control panel and REST API.
    *   **Paho-MQTT:** For communicating with the Zigbee buttons via an MQTT broker.
*   **Hardware:**
    *   Zigbee-compatible wireless buttons.
    *   A Zigbee coordinator connected to a machine running a Zigbee-to-MQTT bridge (like [Zigbee2MQTT](https://www.zigbee2mqtt.io/)).
*   **Audio:**
    *   `mpg123` command-line player for audio playback.

## 🚀 Getting Started

### Prerequisites

*   Python 3
*   An MQTT broker (like Mosquitto)
*   Zigbee2MQTT (or a similar bridge) set up and connected to your Zigbee buttons.
*   `mpg123` installed on the system (`sudo apt-get install mpg123` on Debian/Ubuntu).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lukaszroszczak/inline.git
    cd inline
    ```

2.  **Create a virtual environment and install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install PyQt5 Flask Flask-Cors paho-mqtt
    ```

3.  **Configure the application:**
    *   Edit `gui.ini` to customize the UI appearance if needed.
    *   Update the `button_id_to_column` dictionary in `main_program.py` with the IEEE addresses of your Zigbee buttons. You can find these addresses in your Zigbee2MQTT logs or web UI.

    ```python
    # main_program.py
    self.button_id_to_column = {
        '0x_your_button_1_id': 0,  # Office 1
        '0x_your_button_2_id': 1,  # Office 2
        '0x_your_button_3_id': 2   # Office 3
    }
    ```

4.  **Prepare audio files:**
    *   The application expects pre-generated audio files in the `output/` directory for announcements (e.g., `dingdong.mp3`, `numer.mp3`, `101.mp3`, `gabinet_nr_1.mp3`).
    *   You will need to generate these files using a Text-to-Speech (TTS) engine.

### Running the Application

To start the system, simply run the main program:

```bash
python3 main_program.py
```

This will launch the fullscreen GUI, start the web server on `http://0.0.0.0:5000`, and connect to the MQTT broker.
