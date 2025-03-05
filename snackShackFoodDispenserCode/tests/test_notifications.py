import unittest
from unittest.mock import patch
import notifications  # Import your notifications module

class TestNotifications(unittest.TestCase):

    @patch("notifications.requests.get")  # Mock GET request for ngrok
    def test_get_ngrok_url_success(self, mock_get):
        """Test get_ngrok_url with a valid response."""
        mock_get.return_value.json.return_value = {"tunnels": [{"public_url": "https://mock-ngrok-url.com"}]}
        url = notifications.get_ngrok_url()
        self.assertEqual(url, "https://mock-ngrok-url.com")

    @patch("notifications.requests.get")
    def test_get_ngrok_url_failure(self, mock_get):
        """Test get_ngrok_url failure scenario."""
        mock_get.side_effect = Exception("Network error")
        url = notifications.get_ngrok_url()
        self.assertIsNone(url)

    @patch("notifications.requests.post")  # Mock POST request
    @patch("notifications.get_ngrok_url", return_value="https://mock-ngrok-url.com")
    @patch("notifications.load_users", return_value={"user1": "ExponentPushToken[abcdef]"})
    def test_send_notification_success(self, mock_load_users, mock_get_ngrok, mock_post):
        """Test send_notification with a successful send."""
        mock_post.return_value.json.return_value = {"data": "success"}
        notifications.send_notification("Test Title", "Test Message")
        mock_post.assert_called_once()

    @patch("notifications.requests.post")
    @patch("notifications.get_ngrok_url", return_value=None)
    def test_send_notification_no_ngrok_url(self, mock_get_ngrok, mock_post):
        """Test send_notification when ngrok URL is unavailable."""
        notifications.send_notification("Test", "Message")
        mock_post.assert_not_called()

    @patch("notifications.requests.post")
    @patch("notifications.get_ngrok_url", return_value="https://mock-ngrok-url.com")
    @patch("notifications.load_users", return_value={})
    def test_send_notification_no_users(self, mock_load_users, mock_get_ngrok, mock_post):
        """Test send_notification with no users available."""
        notifications.send_notification("Test", "Message")
        mock_post.assert_not_called()

if __name__ == '__main__':
    unittest.main()
