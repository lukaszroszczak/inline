from gtts import gTTS
import os


def save_tts(text: str, filename: str):
    tts = gTTS(text=text, lang="pl")
    tts.save(filename)
    print(f"Zapisano {filename}")


def generate_audio_files():
    # Kluczowe słowa
    for word in ["numer", "numerek"]:
        save_tts(word, f"{word}.mp3")

    # Liczby 0-99 (wystarczą do składania 100-399)
    for i in range(0, 100):
        save_tts(str(i), f"{i}.mp3")

    # Setki, które wykorzystujemy przy składaniu numerów gabinetów
    for base in [100, 200, 300]:
        save_tts(str(base), f"{base}.mp3")

    # Nazwy gabinetów
    for idx in [1, 2, 3]:
        save_tts(f"gabinet numer {idx}", f"gabinet_nr_{idx}.mp3")


if __name__ == "__main__":
    generate_audio_files()
