# Importation des modules nécessaires
import requests  # Utilisé pour faire des requêtes HTTP
from config import EXPO_PUSH_URL  # URL de l'API Expo pour envoyer des notifications push
from api import load_users  # Fonction supposée être définie dans user_storage.py pour charger les utilisateurs

def get_ngrok_url():
    """Récupère l'URL publique actuelle de ngrok pour le flux vidéo."""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")  # Envoie une requête GET pour récupérer les tunnels ngrok actifs
        ngrok_data = response.json()  # Parse la réponse JSON
        return ngrok_data["tunnels"][0]["public_url"]  # Retourne l'URL publique du premier tunnel
    except Exception as e:
        print("Erreur lors de la récupération de l'URL ngrok:", e)  # Gère les erreurs lors de la récupération
        return None  # Retourne None en cas d'erreur

def send_notification(title, message):
    """Envoie une notification push via Expo."""
    if title is None or message is None:
        print("Titre et message sont requis.")  # Vérifie que le titre et le message sont fournis
        return

    headers = {"Content-Type": "application/json"}  # Spécifie que le corps de la requête sera en JSON
    ngrok_url = get_ngrok_url()  # Récupère l'URL publique de ngrok

    if not ngrok_url:
        print("Impossible d'envoyer la notification : URL ngrok introuvable.")  # Affiche un message si l'URL ngrok est introuvable
        return

    users = load_users()  # Charge la liste des utilisateurs depuis le fichier ou la base de données

    if not users:
        print("Aucun utilisateur trouvé.")  # Si aucun utilisateur n'est trouvé, affiche un message d'erreur
        return

    try:
        # Itère sur les utilisateurs et envoie la notification à chacun
        for key, value in users.items():
            user_id = key  # Récupère l'ID de l'utilisateur
            push_token = value  # Récupère le token de push pour l'utilisateur

            if not push_token:
                print(f"Utilisateur {user_id} non trouvé !")  # Si le token est manquant, affiche un message d'erreur
                return

            # Crée une URL de lien profond pour rediriger l'utilisateur vers l'écran approprié
            deep_link_url = f"snacktest://{user_id}/Feed"

            # Prépare le payload de la notification push
            payload = {
                "to": push_token,  # L'utilisateur cible pour la notification
                "title": title,  # Titre de la notification
                "body": message,  # Corps de la notification
                "data": {
                    "screen": f"{user_id}/Feed",  # Données supplémentaires envoyées avec la notification
                    "message": message,  # Message de la notification
                    "video_url": deep_link_url  # Lien profond pour rediriger l'utilisateur
                },
            }

            # Envoie la notification à Expo via l'API
            response = requests.post(EXPO_PUSH_URL, headers=headers, json=payload)
            print(f"Réponse Expo: {response.json()}")  # Affiche la réponse de l'API Expo
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification: {e}")  # Gère les erreurs lors de l'envoi de la notification
