#!/bin/bash

# Erstelle die wedding-book.service Datei
sudo bash -c 'cat > /lib/systemd/system/wedding-book.service <<EOF
[Unit]
Description=Wedding-Book Service
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/etc/wedding-book/
ExecStart=python /etc/wedding-book/main.py
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
