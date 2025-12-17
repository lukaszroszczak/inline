from gpiozero import Button
from signal import pause

# Ustawienie przycisku na GPIO17
button = Button(17)

# Funkcja wywoływana po naciśnięciu przycisku
def button_pressed():
    print("Przycisk wciśnięty!")

# Przypisanie funkcji do zdarzenia przycisku
button.when_pressed = button_pressed

print("Czekam na wciśnięcie przycisku...")
pause()  # Czeka na zdarzenie bez końca
