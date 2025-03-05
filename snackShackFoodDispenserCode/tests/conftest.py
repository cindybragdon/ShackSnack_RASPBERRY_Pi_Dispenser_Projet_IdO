# conftest.py
import sys
from unittest.mock import MagicMock

# Replace hardware modules with mocks to avoid top-level hardware initialization
# These will be inherited by all test files.
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['gpiozero'] = MagicMock()
sys.modules['picamera2'] = MagicMock()
sys.modules['libcamera'] = MagicMock()
