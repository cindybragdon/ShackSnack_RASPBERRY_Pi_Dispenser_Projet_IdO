# Importation des modules nécessaires
import time  # Pour gérer les pauses dans le programme
import RPi.GPIO as GPIO  # Pour interagir avec les broches GPIO du Raspberry Pi
from gpiozero import MotionSensor  # Pour gérer le capteur PIR de détection de mouvement
from notifications import send_notification  # Pour envoyer des notifications
from config import SERVO_PIN, PIR_SENSOR_PIN  # Importation des paramètres de configuration pour les broches

# Initialisation du servomoteur
GPIO.setmode(GPIO.BCM)  # Utilisation de la numérotation BCM pour les broches GPIO
GPIO.setup(SERVO_PIN, GPIO.OUT)  # Configuration de la broche du servomoteur comme sortie
servo = GPIO.PWM(SERVO_PIN, 50)  # Initialisation du servomoteur avec une fréquence de 50 Hz
servo.start(0)  # Démarre le servomoteur avec un rapport cyclique initial de 0 (repos)

# Initialisation du capteur PIR (passif infrarouge pour la détection de mouvement)
pir = MotionSensor(PIR_SENSOR_PIN)  # Création de l'objet capteur PIR avec la broche définie dans la config

# Fonction pour nourrir l'animal en activant le distributeur de nourriture
def feed_animal(duration=1):
    print(f"Ouverture du distributeur pour {duration} secondes...")  # Affiche un message indiquant la durée d'ouverture
    servo.ChangeDutyCycle(12.5)  # Ouvre le distributeur en ajustant le servomoteur
    time.sleep(duration)  # Attendre pendant la durée spécifiée
    servo.ChangeDutyCycle(2.5)  # Ferme le distributeur
    time.sleep(0.5)  # Petite pause après la fermeture
    servo.ChangeDutyCycle(0)  # Arrête le servomoteur après l'utilisation
    
    # Envoi d'une notification après avoir nourri l'animal
    send_notification("Distributeur activé", f"L'animal a été nourri pendant {duration} secondes.")

# Fonction pour détecter un mouvement de l'animal
def detect_animal():
    tempsRestantAttente = 100  # Temps initial avant de pouvoir envoyer une nouvelle notification
    while True:
        pir.wait_for_motion()  # Attente de la détection de mouvement par le capteur PIR
        print("🕺   Mouvement détecté...")  # Affiche un message quand un mouvement est détecté
        time.sleep(1.5)  # Petite pause pour stabiliser la détection du mouvement
        
        if pir.motion_detected:  # Si un mouvement est effectivement détecté
            send_notification("🚨   Animal détecté", "Un animal a été détecté par le capteur.")  # Envoie une notification de détection
            # Attente d'un certain temps avant d'envoyer une nouvelle notification
            while tempsRestantAttente > 0:
                time.sleep(1)  # Pause d'une seconde
                tempsRestantAttente -= 1  # Réduit le temps d'attente
                print(f"⌛   Prochaine possibilité de notification dans : {tempsRestantAttente} secondes")
            
            tempsRestantAttente = 300  # Réinitialise le temps d'attente à 5 minutes après envoi d'une notification
        
        pir.wait_for_no_motion()  # Attente jusqu'à ce que le mouvement cesse
        print("🐾   Plus de mouvement...")  # Affiche un message quand il n'y a plus de mouvement
