#!/usr/bin/python3
import yaml
import getpass

# Prompt the user for a password
while True:
    # Prompt the user for a password
    password = getpass.getpass("Enter the password that you entered on script of target: ")
    # Prompt the user to confirm the password
    confirm_password = getpass.getpass("Confirm the password: ")

    # Check if the passwords match
    if password == confirm_password:
        break
    else:
        print("Passwords do not match. Please try again.")

# Load the YAML configuration
with open('/etc/prometheus/prometheus.yml', 'r') as file:
    config = yaml.safe_load(file)
# Define the new configuration to add
new_config = {
    'scheme': 'https',
    'basic_auth': {
        'username': 'prometheus',
        'password': password
    },
    'tls_config': {
        'ca_file': '/etc/prometheus/node_exporter.crt'
    }
}

# Find the job_name 'Linux server' and update it with the new configuration
for item in config['scrape_configs']:
    if item.get('job_name') == 'Linux server':
        item.update(new_config)

# Dump the modified configuration back to YAML
with open('/etc/prometheus/prometheus.yml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
