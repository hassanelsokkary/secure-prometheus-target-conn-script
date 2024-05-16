#!/bin/bash

cp ./node_exporter.crt /etc/prometheus/node_exporter.crt
python3 yml_config.py
systemctl restart prometheus
