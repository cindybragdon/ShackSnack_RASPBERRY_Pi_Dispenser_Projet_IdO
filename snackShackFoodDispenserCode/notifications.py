import json
import requests
from config import EXPO_PUSH_TOKEN, EXPO_PUSH_URL

def get_ngrok_url():
    """Récupère l'URL publique actuelle de ngrok"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        ngrok_data = response.json()
        return ngrok_data["tunnels"][0]["public_url"]
    except Exception as e:
        print("Erreur lors de la récupération de l'URL ngrok:", e)
        return None

def send_notification(title, message):
    headers = {"Content-Type": "application/json"}
    payload = {
        "to": EXPO_PUSH_TOKEN,
        "title": title,
        "body": message,
        "data": {"message": message},
    }
    print(f"ExponentPushToken :  {EXPO_PUSH_TOKEN}")
    print(f"Envoi de la notification : {title} - {message}")
    try:
        response = requests.post(EXPO_PUSH_URL, headers=headers, json=payload)
        print("Réponse Expo:", response.json())
    except Exception as e:
        print("Erreur lors de l'envoi de la notification:", e)
