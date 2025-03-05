# Importation des modules nécessaires
from flask import Flask, request, jsonify  # Flask pour créer une API, request pour gérer les requêtes, jsonify pour renvoyer des réponses JSON
from dispenser import feed_animal  # Fonction permettant d'activer le distributeur de nourriture
from api import add_user, save_device_settings  # API pour stocker les informations utilisateur et paramètres de l'appareil
import requests  # Utilisé pour récupérer l'URL publique de ngrok

# Création de l'application Flask
app = Flask(__name__)

@app.route('/register_user', methods=['POST'])
def register_user():
    """
    Stocke l'user_id et le push_token pour les notifications dans le fichier JSON.
    """
    print("Requête reçue pour enregistrer l'utilisateur.")  # Log pour vérifier l'appel de l'endpoint
    data = request.get_json()  # Récupère les données JSON envoyées avec la requête
    user_id = data.get("user_id")  # Extraction de l'ID utilisateur
    push_token = data.get("expo_token")  # Extraction du token Expo pour les notifications push

    if not user_id or not push_token:
        return jsonify({"error": "user_id et expo_token sont requis"}), 400  # Vérifie que les données sont bien fournies

    add_user(user_id, push_token)  # Enregistre l'utilisateur dans l'API de stockage
    return jsonify({"status": "success", "message": "Utilisateur enregistré."})  # Retourne une réponse de succès


@app.route('/feed', methods=['POST'])
def feed():
    """
    Active le distributeur pour nourrir l'animal.
    """
    data = request.get_json()  # Récupère les données JSON envoyées avec la requête
    duration = data.get("duration", 1)  # Durée d'ouverture du distributeur (1s par défaut)
    feed_animal(duration)  # Active le servomoteur du distributeur avec la durée spécifiée
    return jsonify({"status": "success", "message": "Animal nourri."})  # Retourne une confirmation


@app.route('/ngrok_url', methods=['GET'])
def get_ngrok_url():
    """
    Récupère l'URL publique de ngrok et l'affiche.
    """
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")  # Requête vers l'API locale de ngrok
        ngrok_data = response.json()  # Convertit la réponse en JSON
        public_url = ngrok_data["tunnels"][0]["public_url"]  # Récupère l'URL publique du premier tunnel
        return jsonify({"ngrok_url": public_url})  # Retourne l'URL trouvée
    except Exception as e:
        return jsonify({"error": "Impossible de récupérer l'URL ngrok", "details": str(e)})  # Gère les erreurs


@app.route('/device_settings', methods=['POST'])
def set_device_settings():
    """
    Enregistre les paramètres d'un appareil (remplace les paramètres existants).
    """
    data = request.get_json()  # Récupère les données JSON envoyées avec la requête

    # Vérifie que les champs obligatoires sont fournis
    if not data.get("name") or not data.get("isVacationModeActive"):
        return jsonify({"error": "Device name et isVacationModeActive sont requis"}), 400

    save_device_settings(data)  # Sauvegarde les paramètres via l'API
    return jsonify({"status": "success", "message": "Device settings saved."})  # Retourne une confirmation


def start_api():
    """
    Démarre le serveur Flask sur le port 5000 et écoute toutes les interfaces réseau.
    """
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    start_api()  # Exécute l'API si le script est lancé directement
