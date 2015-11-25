"""
Unit tests for server
"""

import subprocess
import unittest
import src.requests as requests
import time

class TestServer(unittest.TestCase):
    """
    Unit tests for server
    """

    def test_status(self):
        """
        Test if server can receive requests
        """

        response = requests.get('http://127.0.0.1:1337')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.text), 'Error with setting code')

        with self.assertRaises(requests.ConnectionError):
            response = requests.get('http://127.0.0.1:1337')

    def setUp(self):
        subprocess.Popen(['nohup', 'python', './src/server.py'])

        # allows server to start
        time.sleep(0.5)


if __name__ == '__main__':
    unittest.main()
