import unittest
import wifi_occupancy_sensor
from flask import Flask

class wifi_occupancy_sensor_tests(unittest.TestCase):
    def setUp(self):
        self.app = wifi_occupancy_sensor.app.test_client()

    def test_mac_match(self):
        res = self.app.get('/occupancy/b8:27:eb:cd:cb:74')
        self.assertEqual(res.data, b'1',msg = "Accurately identify a MAC address")
        res = self.app.get('/occupancy/b8:27:eb:cd:cb:7Z')
        self.assertEqual(res.data, b'0', msg = "Accurately identify when not a MAC address")

if __name__ == '__main__':
    unittest.main()
