import unittest
from unittest.mock import patch, MagicMock
import dispenser  # Import your dispenser module

class TestDispenser(unittest.TestCase):

    @patch("dispenser.send_notification")  # Mock notifications
    @patch("dispenser.servo")  # Patch the module-level servo object
    def test_feed_animal(self, mock_servo, mock_send_notification):
        """Test the feed_animal function."""
        # Create a mock instance for the servo and overwrite the module-level variable.
        mock_servo_instance = MagicMock()
        dispenser.servo = mock_servo_instance

        dispenser.feed_animal(duration=1)  # Call the function under test

        # Verify that the servo commands were issued.
        # (Assuming the actual code calls ChangeDutyCycle(12.5) to open the dispenser,
        #  then 2.5 to close it, and finally 0 to stop the PWM.)
        mock_servo_instance.ChangeDutyCycle.assert_any_call(12.5)
        mock_servo_instance.ChangeDutyCycle.assert_any_call(2.5)
        mock_servo_instance.ChangeDutyCycle.assert_any_call(0)
        
        # Verify the notification call.
        mock_send_notification.assert_called_once_with(
            "Distributeur activé",
            "L'animal a été nourri pendant 1 secondes."
        )

    @patch("dispenser.pir")  # Mock PIR sensor
    @patch("dispenser.send_notification")  # Mock notifications
    def test_detect_animal(self, mock_send_notification, mock_pir):
        """Test the detect_animal function."""
        mock_pir.motion_detected = True  # Simulate that motion is detected
        # Simulate one iteration then raise exception to break out of the loop
        mock_pir.wait_for_motion.side_effect = [None, Exception("Test terminé")]
        mock_pir.wait_for_no_motion.return_value = None

        with self.assertRaises(Exception):  # Expect the exception to stop the loop
            dispenser.detect_animal()

        mock_send_notification.assert_called_with(
            "🚨   Animal détecté",
            "Un animal a été détecté par le capteur."
        )

if __name__ == '__main__':
    unittest.main()
