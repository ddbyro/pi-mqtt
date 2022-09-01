#!/usr/bin/env bash

if [ ! -d "/opt/pi-mqtt-service" ]
then
  mkdir "/opt/pi-mqtt-service/"
  cp -r ./bin /opt/pi-mqtt-service/
  cp -r ./config /opt/pi-mqtt-service/

  cat > /etc/systemd/system/pi-mqtt-service.service <<EOF
[Unit]
Description=pi-mqtt-service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /opt/pi-mqtt-service/bin/pi-mqtt-service.py -p /opt/pi-mqtt-service/config/config.yaml
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
  pip3 install -r requirements.txt
  systemctl daemon-reload
  systemctl enable pi-mqtt-service.service


else
  echo "files already exist. if you are trying to update the service run \"cp ./bin/pi-mqtt-service.py /opt/pi-mqtt-service/bin/\""
fi