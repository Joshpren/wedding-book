#!/bin/bash

sudo apt-get install portaudio19-dev python3-pyaudio
python -m venv /etc/wedding-book/.venv --system-site-packages
source /etc/wedding-book/.venv/bin/activate
pip install -r /etc/wedding-book/requirements.txt
deactivate


# Erstelle die wedding-book.service Datei
sudo bash -c 'cat > /lib/systemd/system/wedding-book.service <<EOF
[Unit]
Description=Wedding-Book Service
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/etc/wedding-book/
ExecStart=/etc/wedding-book/.venv/bin/python /etc/wedding-book/main.py
Environment=PYTHONPATH=/etc/wedding-book/src/
KillSignal=SIGINT
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF'

# Systemd neu laden
systemctl daemon-reload

# Service aktivieren
systemctl enable wedding-book.service

# Service starten
systemctl start wedding-book.service

# Status anzeigen
systemctl status wedding-book.service
