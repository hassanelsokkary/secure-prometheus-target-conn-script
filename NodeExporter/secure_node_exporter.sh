#!/bin/bash

python3 genpass.py
mkdir -p /etc/node_exporter
cp ./config.yaml /etc/node_exporter/
openssl req -x509 \
        -newkey rsa:4096 \
        -nodes \
        -days 365 \
        -keyout /etc/node_exporter/node_exporter.key \
        -out /etc/node_exporter/node_exporter.crt \
        -subj "/O=MyCompany/OU=MyDivision/CN=mydomain.local" \
	-addext "subjectAltName = DNS:mydomain.local"
chown -R node_exporter:node_exporter /etc/node_exporter/
cp /etc/node_exporter/node_exporter.crt .
chown $SUDO_USER ./node_exporter.crt

# Define the path to your systemd unit file
unit_file="/etc/systemd/system/node_exporter.service"

# Define the additional option you want to add
additional_option="--web.config.file=\/etc\/node_exporter\/config.yaml"
# Check if the additional option already exists in the ExecStart line
if grep -q -- "--web\.config\.file=" "$unit_file"; then
    # If it exists, update it
    sed -i -r "s/--web\.config\.file=[[:graph:]]+/$additional_option/g" "$unit_file"
else
    # If it doesn't exist, and ExecStart is  split to multilines "contains \ at of line end",
    # then add new line after ExecStart containing "$additional_option \"
    	
    if grep -q '^ExecStart=[[:print:]]*\\[[:space:]]*$' "$unit_file"; then
    	sed -i -r "/ExecStart=/ s/$/ \\n$additional_option \\\\/" $unit_file
    # If it doesn't exist, and ExectStart is just one line "no \ at end"
    # then add \ to end of line, start new line after it containing "$additional option"
    else
	sed -i -r "/ExecStart=/ s/$/ \\\\\\n$additional_option/" $unit_file
    fi
fi
systemctl daemon-reload
systemctl restart node_exporter
