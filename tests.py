import unittest
import wifi_presence
from flask import Flask

class wifi_presence_tests(unittest.TestCase):
	def setUp(self):
		app = Flask(__name__)
		app.register_blueprint(wifi_presence.wifi_presence)
		self.app = app.test_client()

	def test_mac_match(self):
		res = self.app.get('/b8:27:eb:cd:cb:74')
		self.assertEqual(res.data, b'1',msg	= "Accurately identify a MAC address")
		res = self.app.get('/b8:27:eb:cd:cb:7Z')
		self.assertEqual(res.data, b'0', msg = "Accurately identify when not a MAC address")
		
if __name__ == '__main__':
    unittest.main()