import json
import requests
from config import EXPO_PUSH_TOKEN, EXPO_PUSH_URL

def send_notification(title, message):
    headers = {"Content-Type": "application/json"}
    payload = {
        "to": EXPO_PUSH_TOKEN,
        "title": title,
        "body": message,
        "data": {"message": message},
    }
    print(f"Envoi de la notification : {title} - {message}")
    try:
        response = requests.post(EXPO_PUSH_URL, headers=headers, json=payload)
        print("Réponse Expo:", response.json())
    except Exception as e:
        print("Erreur lors de l'envoi de la notification:", e)
