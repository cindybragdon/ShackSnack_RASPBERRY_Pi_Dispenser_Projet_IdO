import json
import os

USERS_FILE = 'users.json'
DEVICE_SETTINGS_FILE = 'deviceSettings.json'


# Charge les utilisateurs à partir du fichier JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Sauvegarde les utilisateurs dans le fichier JSON
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Ajouter un nouvel utilisateur
def add_user(user_id, push_token):
    users = load_users()
    users[user_id] = push_token
    save_users(users)
    print(f"Utilisateur {user_id} ajouté avec le token {push_token}.")


    # Load device settings
def load_device_settings():
    if os.path.exists(DEVICE_SETTINGS_FILE):
        with open(DEVICE_SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save device settings (overwrite existing settings)
def save_device_settings(device_settings):
    with open(DEVICE_SETTINGS_FILE, 'w') as f:
        json.dump(device_settings, f, indent=4)
