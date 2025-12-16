import pyttsx3

def read_text_in_polish(text):
    engine = pyttsx3.init(driverName='espeak')
    
    try:
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'pl' in voice.id:
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1)

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"Błąd: {e}")

read_text_in_polish("Witaj! To jest test systemu mowy w języku polskim.")
