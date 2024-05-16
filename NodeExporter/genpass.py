#!/usr/bin/python3
import yaml
import bcrypt
import getpass

# Prompt the user for a password
while True:
    # Prompt the user for a password
    password = getpass.getpass("Enter the password: ").encode('utf-8')

    # Prompt the user to confirm the password
    confirm_password = getpass.getpass("Confirm the password: ").encode('utf-8')

    # Check if the passwords match
    if password == confirm_password:
        break
    else:
        print("Passwords do not match. Please try again.")
# Generate bcrypt hash for the provided password
bcrypt_hash = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12)).decode('utf-8')

# Remove any trailing newline characters
bcrypt_hash = bcrypt_hash.rstrip('\n')

# Load the YAML file
with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Update the value associated with the key "prometheus"
data['basic_auth_users']['prometheus'] = bcrypt_hash

# Write the modified data back to the YAML file
with open('config.yaml', 'w') as file:
    yaml.dump(data, file)
