#dispenser.py

import time
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
from notifications import send_notification
from config import SERVO_PIN, PIR_SENSOR_PIN

# Initialisation du servomoteur
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# Initialisation du capteur PIR
pir = MotionSensor(PIR_SENSOR_PIN)

def feed_animal(duration=1):
    print(f"Ouverture du distributeur pour {duration} secondes...")
    servo.ChangeDutyCycle(12.5)  # Ouvre le distributeur
    time.sleep(duration)
    servo.ChangeDutyCycle(2.5)  # Ferme le distributeur
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
    
    send_notification("Distributeur activé", f"L'animal a été nourri pendant {duration} secondes.")

def detect_animal():
    tempsRestantAttente = 100
    while True:
        pir.wait_for_motion()
        print("🕺   Mouvement détecté...")
        time.sleep(1.5)  
        if pir.motion_detected:
            send_notification("🚨   Animal détecté", "Un animal a été détecté par le capteur.")
            while tempsRestantAttente > 0 :
                time.sleep(1)
                tempsRestantAttente -= 1
                print(f"⌛   Prochaine possibilité de notification dans : {tempsRestantAttente} secondes")
            tempsRestantAttente = 300
        pir.wait_for_no_motion()
        print("🐾   Plus de mouvement...")
