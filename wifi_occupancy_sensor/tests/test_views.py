
import json
import os
import sqlite3
import time
import unittest

import wifi_occupancy_sensor

# pylint: disable=line-too-long

NOW = time.time()
expire_time = 3600+NOW
start_time = 500+NOW
end_time = 100+NOW
ALL_DEVICES_RESULT = [
    {'expire_time': expire_time,
     'name': 'example-name',
     'presence_end': end_time,
     'address': '1.2.3.4',
     'user_id': 0,
     'id': '00:00:00:00:00:00',
     'presence_start': start_time},
    {'expire_time': 0,
     'name': None,
     'presence_end': 0,
     'address': '1.2.3.5',
     'user_id': 0,
     'id': '00:00:00:00:00:01',
     'presence_start': 0},
    {'expire_time': 0,
     'name': None,
     'presence_end': 0,
     'address': '1.2.3.6',
     'user_id': 1,
     'id': '00:00:00:00:00:02',
     'presence_start': 0}
]

PRESENT_DEVICES_RESULT = [{'name': 'example-name', 'expire_time': expire_time, 'id': '00:00:00:00:00:00', 'presence_start': start_time, 'address': '1.2.3.4', 'presence_end': end_time, 'device_metadata': {}}]


class ViewsTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.app = wifi_occupancy_sensor.app.test_client()
        self.db_filename = wifi_occupancy_sensor.app.config.get('DATABASE_FILENAME')
        try:
            os.remove(self.db_filename)
        except OSError:
            pass
        conn = sqlite3.connect(self.db_filename)
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL, name TEXT NOT NULL)')
        conn.execute('INSERT INTO users (id, name) VALUES (0, "Alice")')
        conn.execute('INSERT INTO users (id, name) VALUES (1, "Bob")')
        conn.execute('INSERT INTO users (id, name) VALUES (2, "Charlie")')
        conn.execute('CREATE TABLE IF NOT EXISTS devices (id TEXT NOT NULL, user_id INTEGER, name TEXT, address TEXT, expire_time INTEGER, presence_start INTEGER, presence_end INTEGER)')
        conn.execute('INSERT INTO devices (id, user_id, name, address, expire_time, presence_start, presence_end) VALUES (?, ?, ?, ?, ?, ?, ?)', ("00:00:00:00:00:00", 0, "example-name", "1.2.3.4", expire_time, start_time, end_time))
        conn.execute('INSERT INTO devices (id, user_id, name, address, expire_time, presence_start, presence_end) VALUES (?, ?, ?, ?, ?, ?, ?)', ("00:00:00:00:00:01", 0, None, "1.2.3.5", 0, 0, 0))
        conn.execute('INSERT INTO devices (id, user_id, name, address, expire_time, presence_start, presence_end) VALUES (?, ?, ?, ?, ?, ?, ?)', ("00:00:00:00:00:02", 1, None, "1.2.3.6", 0, 0, 0))
        conn.commit()
        conn.close()

    def test_mac_match(self):
        res = self.app.get('/devices?id=00:00:00:00:00:00')
        self.assertEqual(json.loads(res.data.decode()), PRESENT_DEVICES_RESULT, msg="Accurately identify a MAC address")

    def test_rejects_not_mac(self):
        res = self.app.get('/devices?id=b8:27:eb:cd:cb:7Z')
        self.assertEqual(json.loads(res.data.decode()), {'message': '"b8:27:eb:cd:cb:7Z" is not a valid device ID.'}, msg='Accurately identify when not a MAC address')

    def test_rejects_missing_mac(self):
        res = self.app.get('/devices?id=10:00:00:00:00:00')
        self.assertEqual(json.loads(res.data.decode()), {'message': '"10:00:00:00:00:00" is not an existing device.'}, msg='Accurately identify when MAC address is not in the database')

    def test_list_all_devices(self):
        res = self.app.get('/devices')
        self.assertEqual(json.loads(res.data.decode()), ALL_DEVICES_RESULT, msg="Lists all device records")

    def test_list_active_devices(self):
        res = self.app.get('/devices?active=true')
        self.assertEqual(json.loads(res.data.decode()), PRESENT_DEVICES_RESULT, msg="Lists all active devices")

    def test_post_new_user(self):
        pass

    def test_post_new_device(self):
        pass

    def test_put_device(self):
        pass

    def test_delete_device(self):
        pass

    def test_delete_user(self):
        pass

    def tearDown(self):
        #os.remove(self.db_filename)
        pass


if __name__ == '__main__':
    unittest.main()
