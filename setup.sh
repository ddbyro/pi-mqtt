#!/usr/bin/env bash

mkdir -p /opt/pi-mqtt-service/

mv ./pi-mqtt-service.py /usr/bin/
mv ./config /opt/pi-mqtt-service/

cat > /etc/systemd/system/pi-mqtt-service.service <<EOF
[Unit]
Description=GPIO MQTT
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /pi-mqtt-service.py -p /opt/pi-mqtt-service/config.yaml
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

pip3 install -r requirements.txt


