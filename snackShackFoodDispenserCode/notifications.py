#notifications.py
import requests
from config import EXPO_PUSH_URL
from user_storage import load_users  # Supposé être défini dans user_storage.py

def get_ngrok_url():
    """Récupère l'URL publique actuelle de ngrok pour le flux vidéo"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        ngrok_data = response.json()
        return ngrok_data["tunnels"][0]["public_url"]
    except Exception as e:
        print("Erreur lors de la récupération de l'URL ngrok:", e)
        return None

def send_notification(title, message):
    """Envoie une notification push via Expo."""
    if title is None or message is None:
        print("Titre et message sont requis.")
        return

    headers = {"Content-Type": "application/json"}
    ngrok_url = get_ngrok_url()

    if not ngrok_url:
        print("Impossible d'envoyer la notification : URL ngrok introuvable.")
        return



    users = load_users()


    if not users:
        print("Aucun utilisateur trouvé.")
        return

    # Récupère le premier utilisateur
    user_id = list(users.keys())[0]  # Prend la première clé (user_id)
    push_token = users.get(user_id)

    if not push_token:
        print(f"Utilisateur {user_id} non trouvé !")
        return

    deep_link_url = f"snacktest://{user_id}/Feed"

    payload = {
        "to": push_token,
        "title": title,
        "body": message,
        "data": {
            "screen": "{user_id}/Feed",
            "message": message,
            "video_url": deep_link_url
        },
    }

    try:
        response = requests.post(EXPO_PUSH_URL, headers=headers, json=payload)
        print(f"Réponse Expo: {response.json()}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification: {e}")


