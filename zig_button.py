import paho.mqtt.client as mqtt
import json

# Funkcja wywoływana po naciśnięciu przycisku
def update_display(button_id, action):
    print(f"ACTION: Button {button_id} triggered with action {action}")

# Funkcja wywoływana przy niskim poziomie baterii
def low_battery(button_id):
    print(f"LOW BATTERY ALERT: Button {button_id} has battery below 10%")
#ODBIERANIE DANYCH ZIGBEE MQTT
def on_message(client, userdata, message):
    print(f"Odebrano wiadomość: {message.payload.decode()} na temacie {message.topic}")  # Loguj odebrane wiadomości
    try:
        payload = json.loads(message.payload.decode())
        button_id = message.topic.split('/')[-1]  # Pobieramy ID przycisku z tematu
        
        # Sprawdź i wywołaj akcję przycisku
        if 'action' in payload:
            action = payload['action']
            print(f"Wykryto akcję: {action}")  # Dodaj log
            update_display(button_id, action)
        
        # Sprawdź poziom baterii i wywołaj low_battery, jeśli poniżej 10%
        if 'battery' in payload and payload['battery'] < 10:
            print("Niski poziom baterii!")  # Dodaj log
            low_battery(button_id)
    
    except json.JSONDecodeError:
        print("Nieprawidłowa wiadomość JSON:", message.payload.decode())

# Konfiguracja klienta MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)  # Używamy lokalnego brokera

client.on_message = on_message

# Subskrybuj tematy dla wszystkich przycisków
#client.subscribe("zigbee2mqtt/0x3410f4fffeeb85ff")  # Subskrybuj wszystkie urządzenia w Zigbee2MQTT
client.subscribe("zigbee2mqtt/#")  # Subskrybuj wszystkie urządzenia w Zigbee2MQTT

# Uruchomienie klienta w tle
client.loop_start()
print ("Uruchomienie klienta w tle")

try:
    while True:
        pass  # Możesz dodać logikę głównego programu tutaj
except KeyboardInterrupt:
    client.loop_stop()
