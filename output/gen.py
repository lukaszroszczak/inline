from gtts import gTTS
import os

def generate_audio_files():
    # Generowanie plików dla słów "numer" i "numerek"
    words = ["numer", "numerek"]
    
    for word in words:
        tts = gTTS(text=word, lang='pl')
        filename = f"{word}.mp3"  # np. "numer.mp3" lub "numerek.mp3"
        tts.save(filename)
        print(f"Plik {filename} został zapisany.")
    
    # Generowanie plików dla liczb od 1 do 100
    for i in range(1, 101):
        text = f"{i}"  # Tekst dla liczby, np. "35"
        tts = gTTS(text=text, lang='pl')
        
        filename = f"{i}.mp3"  # np. "35.mp3"
        tts.save(filename)
        
        print(f"Plik {filename} został zapisany.")

# Wywołanie funkcji
generate_audio_files()
