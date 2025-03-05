# Importation des modules nécessaires
from flask import Response, Flask  # Flask pour créer l'API Web
import cv2  # OpenCV pour le traitement d'image
from picamera2 import Picamera2  # Picamera2 pour interagir avec la caméra du Raspberry Pi

# Initialisation de la caméra avec Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))  # Configuration de la caméra (résolution 640x480)
picam2.start()  # Démarre la caméra

# Fonction générant les frames vidéo pour le streaming
def generate_frames():
    while True:
        frame = picam2.capture_array()  # Capture une image de la caméra
        _, buffer = cv2.imencode('.jpg', frame)  # Convertit l'image en format JPEG
        frame = buffer.tobytes()  # Convertit le buffer en bytes pour l'envoi via HTTP
        # Génère chaque frame avec un format approprié pour le streaming HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Fonction pour démarrer le serveur de streaming vidéo
def start_stream():
    app = Flask(__name__)  # Création de l'application Flask

    # Route pour le flux vidéo en continu
    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Envoie les frames vidéo sous forme de réponse HTTP

    app.run(host="0.0.0.0", port=5001)  # Démarre le serveur Flask sur le port 5001, accessible sur toutes les interfaces
