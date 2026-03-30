# TODO

## Znane błędy / do naprawy

- Naprawa GUI – `gui.ini`: poprawne wczytywanie kolorów (obecnie `#` traktowane jako komentarz, `header_bg`/`number_bg` puste).
- API start: `/status` powinno sprawdzać `gui_instance` (uniknąć 500 na pierwszych requestach przy starcie wątków).
- Miganie numerów: przerobić `flash_value` na niezależne liczniki/timery per etykieta, żeby szybkie zmiany nie wygaszały migania.
- MQTT: dodać retry/backoff/logowanie przy braku połączenia z brokerem, by przyciski Zigbee wracały po starcie brokera.
- Autostart/systemd: install.sh ma tworzyć użytkownika `inline`, katalog `/home/inline/inline` i venv w tej ścieżce; obecnie `inline.service` wskazuje na nieistniejące ścieżki na świeżym RPi. Rozważyć rotację logów (service.log).
- Bezpieczeństwo panelu: panel Flask nasłuchuje na 0.0.0.0 bez auth – dodać token/IP whitelist jeśli sieć nie jest zaufana.
- `voice.py`: usunąć auto-uruchamianie TTS przy imporcie; zostawić funkcję wywoływaną jawnie.
- Repo vs RPi: plik `main_program.py` w repo jest niezsynchronizowany z działającą wersją `/home/luke/main.py` na RPi (609 linii). Należy zsynchronizować.

## Odporność na zanik zasilania

- **[NAPRAWIONE 2026-03-29]** zigbee2mqtt po zaniku zasilania crashował w nieskończoną pętlę (restart counter 62+) z błędem `EEXIST: file already exists, symlink ... /data/log/current`. Naprawiono przez `ExecStartPre=/bin/rm -f .../data/log/current` w `zigbee2mqtt.service`.
- Firmware dongle'a Zigbee: urządzenie ma EZSP v8 (firmware ~2020). Zalecana aktualizacja do wersji obsługiwanej przez sterownik `ember` (wymaga EZSP v13-14). Do wykonania przy najbliższej wizycie serwisowej z fizycznym dostępem.
- Hardware: rozważyć mini UPS pod Raspberry Pi (np. Waveshare UPS HAT lub powerbank z pass-through) — nagłe odcięcia zasilania to ryzyko uszkodzenia karty SD i podobnych błędów przy starcie usług.

## Dalsze usprawnienia

- `requirements.txt`: dodać plik z zależnościami Pythona (Flask, paho-mqtt, Pillow itp.).
- Logowanie: ujednolicić logowanie w `main.py` (używać `logging` zamiast `print`), by błędy były widoczne w `journalctl`.
