import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Czekam na wciśnięcie przycisku...")
    while True:
        if GPIO.input(17) == GPIO.LOW:
            print("Przycisk wciśnięty!")
            time.sleep(0.3)  # Oczekiwanie, by uniknąć drgań styków

except KeyboardInterrupt:
    print("Koniec programu")
finally:
    GPIO.cleanup()
