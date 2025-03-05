import json
import os

# Définition des fichiers utilisés pour stocker les données
USERS_FILE = 'users.json'  # Fichier contenant les utilisateurs et leurs tokens push
DEVICE_SETTINGS_FILE = 'deviceSettings.json'  # Fichier contenant les paramètres de l'appareil


# Fonction pour charger les utilisateurs à partir du fichier JSON
def load_users():
    # Vérifie si le fichier existe avant de le charger
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)  # Charge le contenu du fichier JSON sous forme de dictionnaire
    return {}  # Retourne un dictionnaire vide si le fichier n'existe pas


# Fonction pour sauvegarder les utilisateurs dans le fichier JSON
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)  # Écrit les données JSON dans le fichier avec une indentation pour la lisibilité


# Fonction pour ajouter un nouvel utilisateur avec son token push
def add_user(user_id, push_token):
    users = load_users()  # Charge les utilisateurs existants
    users[user_id] = push_token  # Ajoute ou met à jour l'utilisateur avec son token
    save_users(users)  # Sauvegarde les données mises à jour
    print(f"Utilisateur {user_id} ajouté avec le token {push_token}.")  # Affiche un message de confirmation


# Fonction pour charger les paramètres de l'appareil à partir du fichier JSON
def load_device_settings():
    if os.path.exists(DEVICE_SETTINGS_FILE):
        with open(DEVICE_SETTINGS_FILE, 'r') as f:
            return json.load(f)  # Charge et retourne les paramètres de l'appareil sous forme de dictionnaire
    return {}  # Retourne un dictionnaire vide si le fichier n'existe pas


# Fonction pour sauvegarder les paramètres de l'appareil dans le fichier JSON (écrase les anciens paramètres)
def save_device_settings(device_settings):
    with open(DEVICE_SETTINGS_FILE, 'w') as f:
        json.dump(device_settings, f, indent=4)  # Sauvegarde les paramètres avec une indentation pour la lisibilité
