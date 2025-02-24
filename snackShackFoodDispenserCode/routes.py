from flask import Flask, request, jsonify
from dispenser import feed_animal
from user_storage import add_user  # Utilisation de votre API de stockage existante
import requests

app = Flask(__name__)

@app.route('/register_user', methods=['POST'])
def register_user():
    """Stocke l'user_id et le push_token pour les notifications dans le fichier JSON"""
    print("Requête reçue pour enregistrer l'utilisateur.")  # Ajoutez un log pour vérifier
    data = request.get_json()
    user_id = data.get("user_id")
    push_token = data.get("expo_token")

    if not user_id or not push_token:
        return jsonify({"error": "user_id et expo_token sont requis"}), 400

    # Enregistrement via votre API persistante
    add_user(user_id, push_token)
    return jsonify({"status": "success", "message": "Utilisateur enregistré."})


@app.route('/feed', methods=['POST'])
def feed():
    """Active le distributeur pour nourrir l'animal"""
    data = request.get_json()
    duration = data.get("duration", 1)
    feed_animal(duration)
    return jsonify({"status": "success", "message": "Animal nourri."})

@app.route('/ngrok_url', methods=['GET'])
def get_ngrok_url():
    """Récupère l'URL publique de ngrok et l'affiche"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        ngrok_data = response.json()
        public_url = ngrok_data["tunnels"][0]["public_url"]
        return jsonify({"ngrok_url": public_url})
    except Exception as e:
        return jsonify({"error": "Impossible de récupérer l'URL ngrok", "details": str(e)})

def start_api():
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    start_api()
