#!/usr/bin/env bash

mkdir /opt/pi-mqtt-service
rm /usr/bin/pi-mqtt-service.py
rm /opt/pi-mqtt-service/config.yaml
cp ./pi-mqtt-service.py /usr/bin/
cp ./config.yaml /opt/pi-mqtt-service/

cat > /etc/systemd/system/pi-mqtt-service.service <<EOF
[Unit]
Description=GPIO MQTT
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /usr/bin/pi-mqtt-service.py -p /opt/pi-mqtt-service/config.yaml
Restart=on-failure
RestartSec=5s
r
[Install]
WantedBy=multi-user.target
EOF

pip3 install -r requirements.txt


