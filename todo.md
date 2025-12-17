# TODO
- Naprawa GUI – `gui.ini`: poprawne wczytywanie kolorów (obecnie `#` traktowane jako komentarz, `header_bg`/`number_bg` puste).
- API start: `/status` powinno sprawdzać `gui_instance` (uniknąć 500 na pierwszych requestach przy starcie wątków).
- Miganie numerów: przerobić `flash_value` na niezależne liczniki/timery per etykieta, żeby szybkie zmiany nie wygaszały migania.
- MQTT: dodać retry/backoff/logowanie przy braku połączenia z brokerem, by przyciski Zigbee wracały po starcie brokera.
- Autostart/systemd: install.sh ma tworzyć użytkownika `inline`, katalog `/home/inline/inline` i venv w tej ścieżce; obecnie `inline.service` wskazuje na nieistniejące ścieżki na świeżym RPi. Rozważyć rotację logów (service.log).
- Bezpieczeństwo panelu: panel Flask nasłuchuje na 0.0.0.0 bez auth – dodać token/IP whitelist jeśli sieć nie jest zaufana.
- `voice.py`: usunąć auto-uruchamianie TTS przy imporcie; zostawić funkcję wywoływaną jawnie.
