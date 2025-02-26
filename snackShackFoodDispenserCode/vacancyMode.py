import time
from datetime import datetime
from api import load_device_settings  # Load device settings from JSON
from dispenser import feed_animal  # Function to activate the feeder

def vacation_mode_thread():
    print("🐾 Vacation Mode Thread Started... Monitoring feeding schedule! 🕒")

    while True:
        print("\n🔄 Checking device settings...")
        device_settings = load_device_settings()

        # If no device settings are found, wait and retry
        if not device_settings:
            print("⚠️ No device settings found. Retrying in 10 seconds... ⏳")
            time.sleep(10)
            continue

        # Check if vacation mode is active
        if not device_settings.get("isVacationModeActive", False):
            print("🛑 Vacation mode is OFF. Waiting 10 seconds before rechecking... ⏳")
            time.sleep(10)
            continue

        print("✅ Vacation mode is ACTIVE! Looking for feeding times... 🍖")
        feeding_times = device_settings.get("feedingTimes", [])
        vacation_feeding_time = device_settings.get("vacationFeedingTime", 2)

        # If there are no feeding times set, notify and wait
        if not feeding_times:
            print("⚠️ No feeding times set! The feeder will not activate. Retrying in 10 seconds... ⏳")
            time.sleep(10)
            continue

        # Get the current time
        now = datetime.now()
        current_day = now.strftime("%A")
        current_hour = now.hour
        current_minute = now.minute

        print(f"📅 Today is: {current_day} | ⏰ Current Time: {current_hour}:{current_minute:02d}")

        # Check if it's time to feed the animal
        for feeding_time in feeding_times:
            for day in feeding_time["days"]:
                if day["day"] == current_day and day["isSelected"]:
                    if feeding_time["hour"] == current_hour and feeding_time["minute"] == current_minute:
                        print(f"🍽️ It's feeding time! Activating the feeder for {vacation_feeding_time} seconds... 🐶🐱")
                        feed_animal(vacation_feeding_time)
                        print("✅ Feeding completed! Waiting 60 seconds to avoid multiple triggers... ⏳")
                        time.sleep(60)  # Prevent multiple triggers in the same minute

        print("🔄 Sleeping for 10 seconds before checking again... ⏳")
        time.sleep(10)  # Check every 10 seconds
