from flask import Flask, request, jsonify
from dispenser import feed_animal

app = Flask(__name__)

@app.route('/feed', methods=['POST'])
def feed():
    data = request.get_json()
    duration = data.get("duration", 1)
    feed_animal(duration)
    return jsonify({"status": "success", "message": "Animal nourri."})

def start_api():
    app.run(host="0.0.0.0", port=5000)
