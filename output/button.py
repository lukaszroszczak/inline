import RPi.GPIO as GPIO
import time


GPIO.cleanup()
# Ustawienie trybu numeracji pinów na BCM (używamy numerów GPIO)
GPIO.setmode(GPIO.BCM)

# Konfiguracja GPIO17 jako wejścia z podciąganiem do góry (pull-up)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Funkcja obsługująca zdarzenie naciśnięcia przycisku
def button_callback(channel):
    print("Przycisk wciśnięty!")

# Rejestracja zdarzenia wciśnięcia przycisku (zbocze opadające)
GPIO.add_event_detect(17, GPIO.FALLING, callback=button_callback, bouncetime=100)

try:
    # Główna pętla programu
    print("Czekam na wciśnięcie przycisku...")
    while True:
        time.sleep(1)  # Program 'czeka' i sprawdza stan przycisku

except KeyboardInterrupt:
    print("Koniec programu")
finally:
    GPIO.cleanup()  # Reset GPIO przed zakończeniem programu
