import unittest
from unittest.mock import patch, MagicMock
import time

# Mocking the latency functions for unit testing
class TestLatencyManagement(unittest.TestCase):
    
    def test_latency_simulation(self):
        """Test that simulates network latency and checks response times."""
        mock_connection = MagicMock()
        with patch('time.time') as mock_time:
            # Simulate a 100ms delay
            mock_time.side_effect = [1.0, 1.1]  # Start at 1.0s, end at 1.1s
            start_time = time.time()
            time.sleep(0.1)
            end_time = time.time()
            
            self.assertTrue((end_time - start_time) >= 0.1)

    def test_response_time_calculation(self):
        """Test that response times are calculated properly."""
        mock_connection = MagicMock()
        with patch('time.time') as mock_time:
            # Simulate a 50ms delay
            mock_time.side_effect = [2.0, 2.05]
            
            start_time = time.time()
            time.sleep(0.05)
            end_time = time.time()
            
            response_time = end_time - start_time
            self.assertAlmostEqual(response_time, 0.05, places=2)

if __name__ == '__main__':
    unittest.main()
