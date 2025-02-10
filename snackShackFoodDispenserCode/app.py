import threading
import signal
import sys
import RPi.GPIO as GPIO
from routes import start_api
from dispenser import detect_animal
from camera import start_stream
import os

def start_ngrok():
    """Lance ngrok pour exposer Flask publiquement"""
    os.system("nohup ngrok http 5000 > /dev/null 2>&1 &")
    print("ngrok démarré. Vérifie l'URL en exécutant 'ngrok status'.")

def handle_exit(sig, frame):
    print("\nArrêt du programme...")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

if __name__ == '__main__':
    start_ngrok()  # Lancer ngrok automatiquement
    
    # Démarrer Flask et la caméra en parallèle
    flask_thread = threading.Thread(target=start_api)
    camera_thread = threading.Thread(target=start_stream)

    flask_thread.daemon = True
    camera_thread.daemon = True

    flask_thread.start()
    camera_thread.start()

    # Lancer la détection de mouvement en boucle
    detect_animal()
