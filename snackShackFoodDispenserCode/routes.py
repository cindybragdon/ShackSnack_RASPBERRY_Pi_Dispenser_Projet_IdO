from flask import Flask, request, jsonify
from dispenser import feed_animal
import os
import requests

app = Flask(__name__)

@app.route('/feed', methods=['POST'])
def feed():
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
