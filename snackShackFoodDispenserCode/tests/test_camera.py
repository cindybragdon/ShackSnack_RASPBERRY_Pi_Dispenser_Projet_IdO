import unittest
from unittest.mock import patch, MagicMock
import camera  # Import your camera module

class TestCameraModule(unittest.TestCase):

    @patch("camera.Picamera2")  # Mock Picamera2
    @patch("camera.cv2")         # Mock OpenCV
    def test_generate_frames(self, mock_cv2, mock_picamera):
        """Test video frame generation."""
        # Set up the Picamera2 mock
        mock_cam_instance = mock_picamera.return_value  
        mock_cam_instance.capture_array.return_value = b"fake_image_data"  # Simulated captured image
        
        # Instead of returning raw bytes, return a mock with a tobytes() method.
        mock_buffer = MagicMock()
        mock_buffer.tobytes.return_value = b"jpeg_encoded_image"
        mock_cv2.imencode.return_value = (True, mock_buffer)  # Simulate JPEG encoding
        
        generator = camera.generate_frames()  # Call the function
        frame = next(generator)  # Get the first frame
        
        self.assertIn(b'Content-Type: image/jpeg', frame)  # Check that the frame has the proper HTTP header

    @patch("camera.Flask")  # Mock Flask
    def test_start_stream(self, mock_flask):
        """Test starting the Flask server."""
        mock_app = mock_flask.return_value  # Simulate Flask app
        mock_app.route.return_value = lambda x: x  # Dummy route decorator
        
        camera.start_stream()  # Call the function
        
        mock_flask.assert_called_once()  # Verify Flask was instantiated
        mock_app.run.assert_called_once_with(host="0.0.0.0", port=5001)  # Verify correct run parameters

if __name__ == '__main__':
    unittest.main()
