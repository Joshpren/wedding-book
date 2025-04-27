#!/bin/bash

# Erstelle die weddingbook.service Datei
sudo bash -c 'cat > /lib/systemd/system/weddingbook.service <<EOF
[Unit]
Description=Wedding Book Service
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/joshua/weddingbook/
ExecStart=sudo python /home/joshua/weddingbook/main.py
KillSignal=SIGINT
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF'

# Systemd neu laden
sudo systemctl daemon-reload

# Service aktivieren
sudo systemctl enable weddingbook.service

# Service starten
sudo systemctl start weddingbook.service

# Status anzeigen
sudo systemctl status weddingbook.service
