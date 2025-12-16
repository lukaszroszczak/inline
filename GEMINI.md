# Gemini CLI Configuration

**Tools:**
[
  {
    "type": "command_line",
    "auto_run": true
  }
]

**Project Context:**
Ten projekt to aplikacja python/flask, używa zigbee do komunikacji z przyciskami, środowiska graficznego do wyświetlania pełnoekranowej aplikacji.
Prace będą prowadzone nad zmianami, usprawnieniami, naprawianiem błędów, dodawaniem funkcji. Całość ma być domyślnie uruchomiona na raspberry pi 5, zdalne polecenia na raspberry możesz wykonywać na hoście luke@192.168.151.181, hasło 3003.tech

---
## Project Description

This project is a **Clinic Queue Management System**. 

It is a Python application that provides a comprehensive solution for managing patient queues in a medical facility with multiple offices.

Key components:
- **`PyQt5` GUI:** A fullscreen display to show the currently called patient number for each office.
- **`Flask` Web Panel:** A web-based interface for remote administration of the queues (e.g., adding/removing patients, changing numbers).
- **`MQTT` and `Zigbee`:** Integrates with wireless Zigbee buttons, allowing doctors to control the queue display with physical button presses.
- **Audio Announcements:** The system plays voice announcements when a new patient is called.

The application is architected to be multi-threaded, ensuring that the GUI, web server, and MQTT client operate without blocking each other. The user interface and internal comments are primarily in Polish.