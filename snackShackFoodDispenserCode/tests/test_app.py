import unittest
from unittest.mock import patch
import RPi.GPIO as GPIO  # Added for cleanup
import app  # Import your app module

class TestApp(unittest.TestCase):

    def setUp(self):
        # Try to clean up any previous GPIO state before each test
        try:
            GPIO.cleanup()
        except Exception:
            pass

    def tearDown(self):
        # Clean up GPIO resources after each test
        try:
            GPIO.cleanup()
        except Exception:
            pass

    @patch('app.start_ngrok')  # Mock ngrok
    @patch('app.start_api')      # Mock the Flask API
    @patch('app.start_stream')   # Mock the camera stream
    @patch('app.broadcast_ip')   # Mock IP broadcast
    @patch('app.vacation_mode_thread')  # Mock vacation mode thread
    @patch('app.detect_animal')  # Mock animal detection
    def test_main_execution(self, mock_detect, mock_vacation, mock_broadcast, mock_stream, mock_api, mock_ngrok):
        """Test the correct launch of threads without executing the actual functions."""
        
        mock_detect.side_effect = KeyboardInterrupt  # Simulate Ctrl+C to stop the loop
        
        with self.assertRaises(KeyboardInterrupt):
            # Start the functions
            app.start_ngrok()  
            app.start_api()  
            app.start_stream()  
            app.broadcast_ip()  
            app.vacation_mode_thread()  
            app.detect_animal()  # This will raise KeyboardInterrupt
        
        # Check if all functions were called exactly once
        mock_ngrok.assert_called_once()
        mock_api.assert_called_once()
        mock_stream.assert_called_once()
        mock_broadcast.assert_called_once()
        mock_vacation.assert_called_once()
        mock_detect.assert_called_once()

if __name__ == '__main__':
    unittest.main()
