import unittest
from unittest.mock import patch
import RPi.GPIO as GPIO  # Added for cleanup
from routes import app  # Import your Flask app

class TestAPI(unittest.TestCase):

    def setUp(self):
        try:
            GPIO.cleanup()
        except Exception:
            pass
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        try:
            GPIO.cleanup()
        except Exception:
            pass

    @patch("api.add_user")  # Mock user addition
    def test_register_user_success(self, mock_add_user):
        """Test registering a valid user."""
        payload = {"user_id": "user123", "expo_token": "ExponentPushToken[abcdef]"}
        response = self.client.post("/register_user", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Utilisateur enregistré."})

    def test_register_user_missing_fields(self):
        """Test failure when required fields are missing."""
        response = self.client.post("/register_user", json={"user_id": "user123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("user_id et expo_token sont requis", response.json["error"])

    @patch("dispenser.feed_animal")
    def test_feed_success(self, mock_feed_animal):
        """Test feeding with a valid duration."""
        response = self.client.post("/feed", json={"duration": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Animal nourri."})

    @patch("requests.get")
    def test_get_ngrok_url_success(self, mock_requests_get):
        """Test retrieving the ngrok URL with a valid response."""
        mock_requests_get.return_value.json.return_value = {"tunnels": [{"public_url": "https://mock-ngrok-url.com"}]}
        response = self.client.get("/ngrok_url")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"ngrok_url": "https://mock-ngrok-url.com"})

    @patch("requests.get", side_effect=Exception("Erreur réseau"))
    def test_get_ngrok_url_failure(self, mock_requests_get):
        """Test retrieving ngrok URL on failure."""
        response = self.client.get("/ngrok_url")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Impossible de récupérer l'URL ngrok", response.json["error"])

    @patch("api.save_device_settings")
    def test_set_device_settings_success(self, mock_save_device_settings):
        """Test saving device settings."""
        payload = {"name": "Distributeur", "isVacationModeActive": True}
        response = self.client.post("/device_settings", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "message": "Device settings saved."})

    def test_set_device_settings_missing_fields(self):
        """Test failure when fields are missing for device settings."""
        response = self.client.post("/device_settings", json={"name": "Distributeur"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Device name et isVacationModeActive sont requis", response.json["error"])

if __name__ == '__main__':
    unittest.main()
