import time
from datetime import datetime
from api import load_device_settings  # Chargement des paramètres de l'appareil depuis un fichier JSON
from dispenser import feed_animal  # Fonction pour activer le distributeur de nourriture

def vacation_mode_thread():
    """
    Thread de surveillance du mode vacances.  
    Vérifie régulièrement si le mode vacances est activé et déclenche l'alimentation automatique 
    aux horaires définis par l'utilisateur.
    """
    print("🐾 Vacation Mode Thread Started... Monitoring feeding schedule! 🕒")

    while True:
        print("\n🔄 Checking device settings...")  
        device_settings = load_device_settings()  # Récupère les paramètres de l'appareil

        # Vérifie si les paramètres de l'appareil sont disponibles, sinon attend et réessaie
        if not device_settings:
            print("⚠️ No device settings found. Retrying in 10 seconds... ⏳")
            time.sleep(10)
            continue  # Reprend l'itération

        # Vérifie si le mode vacances est activé
        if not device_settings.get("isVacationModeActive", False):
            print("🛑 Vacation mode is OFF. Waiting 10 seconds before rechecking... ⏳")
            time.sleep(10)
            continue

        print("✅ Vacation mode is ACTIVE! Looking for feeding times... 🍖")
        feeding_times = device_settings.get("feedingTimes", [])  # Liste des heures de repas
        vacation_feeding_time = device_settings.get("vacationFeedingTime", 2)  # Durée d'activation du distributeur

        # Vérifie si des heures de repas sont configurées
        if not feeding_times:
            print("⚠️ No feeding times set! The feeder will not activate. Retrying in 10 seconds... ⏳")
            time.sleep(10)
            continue

        # Récupère l'heure actuelle
        now = datetime.now()
        current_day = now.strftime("%A")  # Jour actuel en texte (ex: "Monday")
        current_hour = now.hour  # Heure actuelle
        current_minute = now.minute  # Minute actuelle

        print(f"📅 Today is: {current_day} | ⏰ Current Time: {current_hour}:{current_minute:02d}")

        # Vérifie si l'heure actuelle correspond à un moment de nourrissage programmé
        for feeding_time in feeding_times:
            for day in feeding_time["days"]:
                if day["day"] == current_day and day["isSelected"]:  # Vérifie si le jour est actif
                    if feeding_time["hour"] == current_hour and feeding_time["minute"] == current_minute:
                        print(f"🍽️ It's feeding time! Activating the feeder for {vacation_feeding_time} seconds... 🐶🐱")
                        feed_animal(vacation_feeding_time)  # Active le distributeur
                        print("✅ Feeding completed! Waiting 60 seconds to avoid multiple triggers... ⏳")
                        time.sleep(60)  # Évite les déclenchements multiples dans la même minute

        print("🔄 Sleeping for 10 seconds before checking again... ⏳")
        time.sleep(10)  # Vérifie toutes les 10 secondes
