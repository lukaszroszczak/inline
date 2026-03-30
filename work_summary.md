# Podsumowanie bieżących prac

## 1. Konfiguracja projektu i repozytorium GitHub

*   Utworzono repozytorium GitHub na koncie użytkownika (`git@github.com:lukaszroszczak/inline.git`).
*   Zainicjowano lokalne repozytorium Git i wykonano początkowy commit.
*   Skonfigurowano nazwę użytkownika i adres e-mail Git.
*   Usunięto zbędne pliki i katalogi (`2802_main.py`, `ok_1902.py`, `test.py`, `logo_test.png`, `back/`, `ok_2802_back/`).
*   Plik `.gitignore` został zaktualizowany w celu prawidłowego ignorowania niepotrzebnych plików i śledzenia `GEMINI.md`.

## 2. Przygotowanie środowiska i uruchomienie aplikacji na Raspberry Pi

*   **Skrypt instalacyjny (`install.sh`)**:
    *   Został stworzony i wielokrotnie aktualizowany w celu automatyzacji instalacji zależności systemowych i pakietów Pythona.
    *   Uwzględnia instalację `python3-venv`, `mpg123`, `mosquitto`, `qtbase5-dev`, `python3-pyqt5`.
    *   Tworzy środowisko wirtualne z dostępem do systemowych pakietów (`--system-site-packages`).
    *   Instaluje pakiety Pythona: `Flask`, `Flask-Cors`, `paho-mqtt`, `Pillow`.
*   **Rozwiązanie problemów z uruchomieniem GUI**:
    *   Aplikacja została pomyślnie uruchomiona na wyświetlaczu Raspberry Pi w trybie interaktywnym (przez SSH).
    *   Rozwiązano problemy z autoryzacją X11 (`Authorization required`), przekazując `DISPLAY=:0` oraz `XAUTHORITY` do środowiska `sudo`.
    *   Rozwiązano problemy z dostępem do sprzętu graficznego (`drmModeGetResources failed`), uruchamiając aplikację jako `root` i ustawiając `QT_QPA_PLATFORM=linuxfb` (wcześniej), a potem `QT_QPA_PLATFORM=xcb` (ostatecznie działająca konfiguracja).
*   **Usługa `systemd`**:
    *   Utworzono plik usługi `inline.service` do automatycznego uruchamiania aplikacji przy starcie systemu i zarządzania nią.
    *   Skrypt `install.sh` został zaktualizowany o kroki instalacji i włączania tej usługi `systemd`.
    *   Na RPi działa jako `przychodnia_gui.service` (nie `inline.service`) uruchamiając `/home/luke/main.py`.

## 3. Dokumentacja

*   Plik `README.md` został stworzony i zaktualizowany o szczegółowy opis projektu, funkcji, stosu technologicznego oraz instrukcji instalacji i zarządzania aplikacją jako usługą `systemd`. Dodano sekcję o dostępie do interfejsu webowego.
*   Plik `GEMINI.md` został zaktualizowany o opis projektu.
*   Utworzono `SZYBKI-START.txt` zawierający skróconą instrukcję obsługi.
*   Dodano komentarze do `gui.ini`, wyjaśniające każdy parametr.

## 4. Diagnoza i naprawa awarii po zaniku zasilania (2026-03-29)

System przestał działać po zaniku zasilania ok. 2026-03-23. Diagnoza przez SSH (luke@10.8.0.13).

### Przyczyna główna

zigbee2mqtt przy każdym starcie tworzy symlink `current` w katalogu logów (`/home/luke/zigbee2mqtt/data/log/current`). Po nagłym odcięciu prądu symlink zostaje na dysku. Przy kolejnym uruchomieniu próba stworzenia go ponownie kończy się błędem `EEXIST: file already exists` → exit-code 1 → `Restart=always` → pętla crash/restart (zaobserwowano restart counter = 62+).

### Zastosowana naprawa

Dodano do `/etc/systemd/system/zigbee2mqtt.service`:
```
ExecStartPre=/bin/rm -f /home/luke/zigbee2mqtt/data/log/current
RestartSec=5
```
Plik `zigbee2mqtt.service` z tą poprawką dodano do repozytorium.

### Dodatkowe ustalenia

*   Dongle Zigbee ma firmware EZSP v8 (ok. 2020). Próba przełączenia na nowszy sterownik `ember` nie powiodła się — wymaga EZSP v13-14. Urządzenie pozostaje na sterowniku `ezsp` (deprecated, ale działający). Zalecana aktualizacja firmware przy okazji wizyty serwisowej.
*   Zmieniono `log_level` w konfiguracji zigbee2mqtt z `warning` na `info` dla lepszej diagnostyki.
*   Potwierdzono działanie MQTT: wszystkie 4 urządzenia Zigbee (3 przyciski SNZB-01P, 1 czujnik SNZB-06P) rejestrowane poprawnie, akcje przycisków docierają do aplikacji.
*   Główna aplikacja (`/home/luke/main.py`) uruchomiona jako `przychodnia_gui.service`, działa stabilnie.

## 5. Bieżący status

*   System działa stabilnie po naprawie z 2026-03-29.
*   Otwarte zadania — patrz `todo.md`.

## 6. Dalsze kroki

*   Zsynchronizować `main_program.py` w repo z działającą wersją `/home/luke/main.py` na RPi.
*   Aktualizacja firmware dongle'a Zigbee (wymaga fizycznego dostępu).
*   Rozważyć mini UPS dla Raspberry Pi.
*   Przejrzeć otwarte punkty z `todo.md`.
