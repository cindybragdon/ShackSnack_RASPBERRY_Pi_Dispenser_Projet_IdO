# Importation des modules nécessaires
import threading
import signal
import sys
import RPi.GPIO as GPIO
from routes import start_api  # Fonction pour démarrer l'API Flask
from dispenser import detect_animal  # Fonction pour détecter l'animal
from camera import start_stream  # Fonction pour démarrer le flux vidéo de la caméra
from sendIP import broadcast_ip  # Fonction pour diffuser l'IP du Raspberry Pi
from vacancyMode import vacation_mode_thread  # Fonction pour activer le mode vacances
import os

# Fonction pour lancer ngrok afin d'exposer Flask publiquement
def start_ngrok():
    """Lance ngrok pour exposer Flask publiquement"""
    os.system("nohup ngrok http 5000 > /dev/null 2>&1 &")  # Exécution de ngrok en arrière-plan
    print("ngrok démarré. Vérifie l'URL en exécutant 'ngrok status'.")  # Message de confirmation

# Fonction pour gérer l'arrêt du programme proprement
def handle_exit(sig, frame):
    print("\nArrêt du programme...")  # Message affiché lors de l'arrêt
    GPIO.cleanup()  # Nettoyage des ressources GPIO
    sys.exit(0)  # Arrêt du programme avec succès

# Enregistrement de la fonction handle_exit pour intercepter l'interruption SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handle_exit)

# Point d'entrée principal du programme
if __name__ == '__main__':
    start_ngrok()  # Lancer ngrok automatiquement pour exposer l'API Flask publiquement
    
    # Démarrer les différentes parties du programme dans des threads parallèles
    flask_thread = threading.Thread(target=start_api)  # Thread pour démarrer l'API Flask
    camera_thread = threading.Thread(target=start_stream)  # Thread pour démarrer le flux de la caméra
    sendIP_thread = threading.Thread(target=broadcast_ip)  # Thread pour diffuser l'IP
    vacancyMode_thread = threading.Thread(target=vacation_mode_thread)  # Thread pour gérer le mode vacances

    # Configuration des threads en mode "daemon" pour qu'ils se terminent automatiquement à l'arrêt du programme
    flask_thread.daemon = True
    camera_thread.daemon = True
    sendIP_thread.daemon = True
    vacancyMode_thread.daemon = True

    # Démarrer les threads
    flask_thread.start()
    camera_thread.start()
    sendIP_thread.start()
    vacancyMode_thread.start()

    # Lancer la détection de l'animal de manière continue (fonction bloquante)
    detect_animal()
