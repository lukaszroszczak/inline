import sys
import os
import time
import threading
import queue
import json
import subprocess
import configparser  # <-- do wczytywania pliku .ini

# Flask
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# MQTT
import paho.mqtt.client as mqtt

# PyQt
from PyQt5 import QtCore, QtGui, QtWidgets

# Pillow
from PIL import Image

#################################
# Flask app
#################################

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')  # jeśli masz plik static/index.html

@app.route('/status', methods=['GET'])
def status():
    return jsonify(gui_instance.get_status())

@app.route('/office/<int:office_id>', methods=['GET'])
def office_view(office_id):
    if gui_instance is None:
        return jsonify({'success': False, 'error': 'GUI instance is not initialized'}), 500

    if 1 <= office_id <= 3:
        office_data = {
            'office_id': office_id,
            'number': gui_instance.numbers[office_id - 1],
            'queue': gui_instance.office_queues[office_id - 1]
        }
        return render_template('office.html', office=office_data)

    return jsonify({'success': False, 'error': 'Invalid office ID'}), 400

@app.route('/office/<int:office_id>/action/<string:action>', methods=['POST'])
def office_action(office_id, action):
    if 1 <= office_id <= 3 and action in ["increment", "decrement", "reset"]:
        command_queue.put({'type': action, 'office_id': office_id})
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid request'}), 400

@app.route('/office/<int:office_id>/add_number', methods=['POST'])
def add_number(office_id):
    if 1 <= office_id <= 3:
        command_queue.put({'type': 'add_number', 'office_id': office_id})
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid office ID'}), 400

@app.route('/office/<int:office_id>/remove_number', methods=['POST'])
def remove_number(office_id):
    if 1 <= office_id <= 3:
        data = request.get_json()
        if not data or 'number' not in data:
            return jsonify({'success': False, 'error': 'Invalid request'}), 400
        num = data.get('number')
        command_queue.put({'type': 'remove_number', 'office_id': office_id, 'number': num})
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Invalid office ID'}), 400

def flask_thread():
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)


#################################
# MQTT
#################################

def on_mqtt_message(client, userdata, message):
    print(f"[MQTT] Otrzymano: {message.payload.decode()} na temacie {message.topic}")
    try:
        payload = json.loads(message.payload.decode())
        button_id = message.topic.split('/')[-1]

        if 'action' in payload:
            action = payload['action']
            print(f"[MQTT] Wykryto akcję: {action}")
            command_queue.put({'type': 'update_display', 'button_id': button_id, 'action': action})

        if 'battery' in payload and payload['battery'] < 10:
            print("[MQTT] Niski poziom baterii!")
            command_queue.put({'type': 'low_battery', 'button_id': button_id})

    except json.JSONDecodeError:
        print("[MQTT] Nieprawidłowa wiadomość JSON:", message.payload.decode())

def mqtt_thread():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    client.on_message = on_mqtt_message
    client.subscribe("zigbee2mqtt/#")
    client.loop_forever()

#################################
# Global queue + reference
#################################
command_queue = queue.Queue()
gui_instance = None

#################################
# Funkcja do ładowania pliku INI
#################################

def load_config(path="gui.ini"):
    config = configparser.ConfigParser()
    config.read(path)
    return config


#################################
# PyQt
#################################

class NumberLabel(QtWidgets.QLabel):
    """Proste QLabel do wyświetlania liczby."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def setNumber(self, value: int):
        self.setText(str(value))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, command_queue, config):
        super().__init__()
        self.command_queue = command_queue
        self.config = config

        # -------------------------
        # Odczyt parametrów z config
        # -------------------------

        # Domyślny alpha (przezroczystość):
        self.alpha = self.config.getfloat("UI", "alpha", fallback=0.0)

        # Bazowa wysokość do skalowania (np. 1080):
        self.design_height = self.config.getint("UI", "design_height", fallback=1080)
        self.scale_factor = 1.0  # Będzie aktualizowana w updateScaling()

        # Globalny mnożnik:
        self.global_scale_multiplier = self.config.getfloat("UI", "global_scale_multiplier", fallback=1.6)

        # Marginesy, wysokość paska
        self.base_margin_left = self.config.getint("UI", "base_margin_left", fallback=165)
        self.base_margin_right = self.config.getint("UI", "base_margin_right", fallback=165)
        self.base_header_height = self.config.getint("UI", "base_header_height", fallback=150)

        # Rozmiary czcionek
        self.base_font_header = self.config.getint("UI", "base_font_header", fallback=48)
        self.base_font_number = self.config.getint("UI", "base_font_number", fallback=40)
        self.base_font_title = self.config.getint("UI", "base_font_title", fallback=48)
        self.base_font_footer = self.config.getint("UI", "base_font_footer", fallback=36)

        # Kolory
        self.header_bg = self.config.get("UI", "header_bg", fallback="#0b6178")
        self.number_bg = self.config.get("UI", "number_bg", fallback="#0b6178")

        # -------------------------
        # Pozostałe pola
        # -------------------------

        # Zakresy i początkowe wartości
        self.min_values = [100, 200, 300]
        self.max_values = [199, 299, 399]
        self.numbers = [100, 200, 300]

        # Kolejka dźwięków
        self.sound_queue = queue.Queue()
        self.is_playing = False

        # Kolejki pacjentów
        self.office_queues = [
            [{'time': '08:00', 'number': 1}, {'time': '08:15', 'number': 2}],
            [{'time': '08:00', 'number': 1}],
            [{'time': '08:00', 'number': 1}]
        ]

        # Mapowanie ID przycisków
        self.button_id_to_column = {
            '0x3410f4fffeeb85ff': 0,
            '0x048727fffedab18b': 1,
            '0x048727fffeafb6d6': 2
        }

        self.setWindowTitle("Przychodnia - PyQt (Dynamic Scaling)")

        # Wczytanie pliku do tła (jeżeli istnieje)
        self.original_logo = None
        self.bg_pixmap = QtGui.QPixmap()
        image_path = "logo.png"
        if os.path.isfile(image_path):
            self.original_logo = Image.open(image_path).convert("RGBA")

        # 1. Tworzymy interfejs
        self.setup_ui()

        # 2. Ustawienie stylów
        self.updateScaling()
        self.updateFonts()
        self.updateBackground()

        # Timery: obsługa kolejki + zegar
        self.queue_timer = QtCore.QTimer(self)
        self.queue_timer.setInterval(100)
        self.queue_timer.timeout.connect(self.process_queue)
        self.queue_timer.start()

        self.datetime_timer = QtCore.QTimer(self)
        self.datetime_timer.setInterval(1000)
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start()
        self.update_datetime()

        # ESC -> zamknięcie
        QtWidgets.QShortcut(QtGui.QKeySequence("Escape"), self, self.close)

    def setup_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Główny layout pionowy
        self.main_layout = QtWidgets.QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # -- Górny pasek (header_frame) - z pliku ini odczytujemy kolor
        self.header_frame = QtWidgets.QFrame()
        self.header_frame.setObjectName("HeaderFrame")
        self.header_frame.setStyleSheet(f"""
            QFrame#HeaderFrame {{
                background-color: {self.header_bg};
            }}
        """)
        self.header_layout = QtWidgets.QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(20, 20, 20, 20)
        self.header_layout.setSpacing(10)

        self.header_layout.addStretch()

        self.logo_label = QtWidgets.QLabel()
        self.header_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignCenter)

        self.title_label = QtWidgets.QLabel('Praktyka Lekarza Rodzinnego "Życie"')
        self.header_layout.addWidget(self.title_label, 0, QtCore.Qt.AlignCenter)

        self.header_layout.addStretch()

        self.main_layout.addWidget(self.header_frame, 0)

        # -- Środek
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        # Domyślnie minimalne marginesy, docelowe w updateFonts():
        self.content_layout.setContentsMargins(0, 20, 0, 20)
        self.content_layout.setSpacing(10)

        # Wiersze:
        self.row1 = self.create_office_row("Gabinet nr 1", self.numbers[0])
        self.row2 = self.create_office_row("Gabinet nr 2", self.numbers[1])
        self.row3 = self.create_office_row("Gabinet nr 3", self.numbers[2])

        self.hline1 = self.make_hline()
        self.hline2 = self.make_hline()

        self.content_layout.addWidget(self.row1, 1)
        self.content_layout.addWidget(self.hline1, 0)
        self.content_layout.addWidget(self.row2, 1)
        self.content_layout.addWidget(self.hline2, 0)
        self.content_layout.addWidget(self.row3, 1)

        # Stopka (zegar)
        self.footer_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.content_layout.addWidget(self.footer_label, 0, QtCore.Qt.AlignBottom)

        self.main_layout.addWidget(self.content_widget, 1)

    def create_office_row(self, gab_text, initial_value):
        row_widget = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row_widget)
        row_layout.setSpacing(10)
        row_layout.setContentsMargins(0, 0, 0, 0)

        gab_label = QtWidgets.QLabel(gab_text)
        num_label = NumberLabel()
        num_label.setNumber(initial_value)

        if "1" in gab_text:
            self.gab1_label = gab_label
            self.num1_label = num_label
        elif "2" in gab_text:
            self.gab2_label = gab_label
            self.num2_label = num_label
        elif "3" in gab_text:
            self.gab3_label = gab_label
            self.num3_label = num_label

        row_layout.addWidget(gab_label, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        row_layout.addStretch()
        row_layout.addWidget(num_label, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        return row_widget

    def make_hline(self):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Plain)
        line.setLineWidth(1)
        line.setStyleSheet("color: #C0C0C0; background-color: #C0C0C0;")
        return line

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateScaling()
        self.updateFonts()
        self.updateBackground()

    def updateScaling(self):
        """
        Skalowanie oparte tylko na wysokości ekranu:
        scale_factor = current_height / design_height
        """
        h = self.height()
        if h < 10:
            self.scale_factor = 1.0
            return

        self.scale_factor = h / self.design_height
        # Dodatkowy globalny współczynnik z pliku ini:
        self.scale_factor *= self.global_scale_multiplier

    def updateFonts(self):
        """
        Przeliczamy style w px w oparciu o scale_factor i wartości wczytane z INI.
        """
        sf = self.scale_factor

        # Górny pasek (wysokość)
        header_height = int(self.base_header_height * sf)
        self.header_frame.setFixedHeight(header_height)

        # Logo (skalowane do ~60% paska)
        if os.path.isfile("logo.png"):
            pix = QtGui.QPixmap("logo.png")
            desired_logo_height = int(header_height * 0.6)
            self.logo_label.setPixmap(pix.scaledToHeight(desired_logo_height, QtCore.Qt.SmoothTransformation))

        # Tytuł
        font_title_px = int(self.base_font_title * sf)
        self.title_label.setStyleSheet(f"""
            color: white;
            font-size: {font_title_px}px;
            font-weight: bold;
        """)

        # Marginesy w content_layout (lewy i prawy)
        margin_left = int(self.base_margin_left * sf)
        margin_right = int(self.base_margin_right * sf)
        self.content_layout.setContentsMargins(margin_left, 20, margin_right, 20)

        # Napisy "Gabinet nr X"
        font_gab_px = int(self.base_font_header * sf)
        style_gab = f"font-size: {font_gab_px}px; color: black; font-weight: bold;"
        self.gab1_label.setStyleSheet(style_gab)
        self.gab2_label.setStyleSheet(style_gab)
        self.gab3_label.setStyleSheet(style_gab)

        # Numer (turkusowe tło, wczytane z config)
        font_num_px = int(self.base_font_number * sf)
        style_num = f"""
            background-color: {self.number_bg};
            color: white;
            font-size: {font_num_px}px;
            font-weight: bold;
            padding: {int(10*sf)}px {int(20*sf)}px;
            border-radius: {int(6*sf)}px;
        """
        self.num1_label.setStyleSheet(style_num)
        self.num2_label.setStyleSheet(style_num)
        self.num3_label.setStyleSheet(style_num)

        # Zegar (stopka)
        font_footer_px = int(self.base_font_footer * sf)
        self.footer_label.setStyleSheet(f"""
            font-size: {font_footer_px}px;
            color: black;
        """)

    def updateBackground(self):
        if self.original_logo is None:
            return

        w = self.width()
        h = self.height()
        if w < 2 or h < 2:
            return

        img_resized = self.original_logo.resize((w, h), Image.Resampling.LANCZOS)
        white_bg = Image.new("RGBA", (w, h), (255,255,255,255))
        blended = Image.blend(white_bg, img_resized, self.alpha)

        data = blended.tobytes("raw", "RGBA")
        qimage = QtGui.QImage(data, w, h, QtGui.QImage.Format_RGBA8888)
        self.bg_pixmap = QtGui.QPixmap.fromImage(qimage)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if not self.bg_pixmap.isNull():
            painter.drawPixmap(0, 0, self.bg_pixmap)
        super().paintEvent(event)

    ##################################
    # Logika kolejki (MQTT, Flask, dźwięki)
    ##################################

    def process_queue(self):
        while True:
            try:
                command = command_queue.get_nowait()
            except queue.Empty:
                break

            if command['type'] == 'update_display':
                self.update_display(command['button_id'], command['action'])

            elif command['type'] == 'low_battery':
                self.show_low_battery_alert(command['button_id'])

            elif command['type'] == 'increment':
                i = command['office_id'] - 1
                new_val = self.numbers[i] + 1
                if new_val <= self.max_values[i]:
                    self.numbers[i] = new_val
                self.refresh_number(i)
                self.flash_value(i)
                self.play_sound_sequence(self.numbers[i], i)

            elif command['type'] == 'decrement':
                i = command['office_id'] - 1
                new_val = self.numbers[i] - 1
                if new_val >= self.min_values[i]:
                    self.numbers[i] = new_val
                self.refresh_number(i)
                self.flash_value(i)
                self.play_sound_sequence(self.numbers[i], i)

            elif command['type'] == 'reset':
                i = command['office_id'] - 1
                self.numbers[i] = self.min_values[i]
                self.refresh_number(i)
                # (opcjonalnie) flash_value i dźwięk:

            elif command['type'] == 'add_number':
                office_id = command['office_id'] - 1
                new_number = len(self.office_queues[office_id]) + 1
                current_time = time.strftime("%H:%M")
                self.office_queues[office_id].append({
                    'time': current_time,
                    'number': new_number
                })

            elif command['type'] == 'remove_number':
                office_id = command['office_id'] - 1
                num_to_remove = command['number']
                self.office_queues[office_id] = [
                    x for x in self.office_queues[office_id]
                    if x['number'] != num_to_remove
                ]

    def refresh_number(self, idx):
        if idx == 0:
            self.num1_label.setNumber(self.numbers[idx])
        elif idx == 1:
            self.num2_label.setNumber(self.numbers[idx])
        elif idx == 2:
            self.num3_label.setNumber(self.numbers[idx])

    def update_display(self, button_id, action):
        column_index = self.button_id_to_column.get(button_id)
        if column_index is not None:
            if action in ('single', 'double'):
                new_val = self.numbers[column_index] + 1
                if new_val <= self.max_values[column_index]:
                    self.numbers[column_index] = new_val
            elif action == 'long':
                new_val = self.numbers[column_index] - 1
                if new_val >= self.min_values[column_index]:
                    self.numbers[column_index] = new_val
            else:
                print(f"Nieznana akcja: {action}")
                return

            self.refresh_number(column_index)
            self.flash_value(column_index)
            self.play_sound_sequence(self.numbers[column_index], column_index)
        else:
            print(f"Nieznany button_id: {button_id}")

    def flash_value(self, idx, flashes=3, interval=300):
        self.flash_count = flashes * 2

        label_map = {0: self.num1_label, 1: self.num2_label, 2: self.num3_label}
        label = label_map[idx]

        def toggle():
            nonlocal label
            if self.flash_count > 0:
                is_visible = label.isVisible()
                label.setVisible(not is_visible)
                self.flash_count -= 1
            else:
                label.setVisible(True)
                timer.stop()

        timer = QtCore.QTimer(self)
        timer.setInterval(interval)
        timer.timeout.connect(toggle)
        timer.start()

    def play_sound_sequence(self, number, button_id):
        def enqueue_sounds():
            sound_files = [
                os.path.join('output', 'dingdong.mp3'),
                os.path.join('output', 'numer.mp3'),
                os.path.join('output', f'{number}.mp3'),
                os.path.join('output', f'gabinet_nr_{button_id + 1}.mp3')
            ]
            self.sound_queue.put(sound_files)
            self.process_sound_queue()

        threading.Thread(target=enqueue_sounds).start()

    def process_sound_queue(self):
        if self.is_playing or self.sound_queue.empty():
            return

        self.is_playing = True
        sound_files = self.sound_queue.get()

        def play_sounds():
            for sf in sound_files:
                if os.path.exists(sf):
                    subprocess.run(['mpg123', sf],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                else:
                    print(f"Błąd: Plik {sf} nie istnieje.")

            self.is_playing = False
            self.process_sound_queue()

        threading.Thread(target=play_sounds).start()

    def show_low_battery_alert(self, button_id):
        print(f"ALERT: Niski poziom baterii w przycisku {button_id}")

    def get_status(self):
        return {
            'numbers': self.numbers,
            'queues': self.office_queues
        }

    def update_datetime(self):
        current_time = time.strftime("%H:%M:%S %d:%m:%Y")
        self.footer_label.setText(current_time)


def main():
    # (1) Włączamy HiDPI
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # (2) Wczytujemy config z pliku gui.ini
    config = load_config("gui.ini")

    # (3) Uruchamiamy wątki: MQTT + Flask
    threading.Thread(target=mqtt_thread, daemon=True).start()
    threading.Thread(target=flask_thread, daemon=True).start()

    # (4) Start PyQt
    app = QtWidgets.QApplication(sys.argv)

    global gui_instance
    gui = MainWindow(command_queue, config)  # przekazujemy config do MainWindow
    gui_instance = gui

    gui.showFullScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
