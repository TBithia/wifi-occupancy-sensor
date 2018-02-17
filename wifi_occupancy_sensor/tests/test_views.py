
import json
import datetime
import unittest

from wifi_occupancy_sensor import app, db, api, users, devices, models
from wifi_occupancy_sensor.tests.testdata import TEST_CONFIG


# pylint: disable=line-too-long
"""To regenerate test data:

    >>> from wifi_occupancy_sensor.test import testdata
    >>> active_device = testdata.AliceDevice1(Alice, expire_time_timestamp='NOW+3600', presence_start_timestamp='NOW+500', presence_end_timestamp='NOW+200')
    >>> alice = testdata.Alice(devices=[active_device])
    >>> bob = testdata.Bob(devices=[testdata.BobDevice1(Bob), testdata.BobDevice2])
    >>> all_devices_result = [x.request_result for x in  BOB.devices+ ALICE.devices]
    >>> print('ACTIVE_DEVICE =', active_device)
    # incorrect result >>> print('ACTIVE_DEVICES_RESULT =', [active_device])
    # incorrect result >>> print('ALL_DEVICES_RESULT =', json.dumps(all_devices_result, sort_keys=True))
    # Inside setUp()
    >>> print(alice.constructor)
    >>> print(bob.constructor)

"""

NOW = int(datetime.datetime.now().timestamp())
ACTIVE_DEVICE_RESULT = {'name': 'Alice phone 01', 'expire_time': NOW + 3600, 'presence_start': NOW + 500, 'presence_end': NOW + 200, 'user_id': 0, 'id': '00:00:00:00:00:11', 'properties': {'device_option0': 'value10', 'device_option1': 'value11'}}
ACTIVE_DEVICES_RESULT = [{"expire_time": NOW + 3600, "id": "00:00:00:00:00:11", "name": "Alice phone 01", "presence_end": NOW + 200, "presence_start": NOW + 500, "properties": {"device_option0": "value10", "device_option1": "value11"}, "user_id": 0}]
ALL_DEVICES_RESULT = [{"expire_time": 0, "id": "00:00:00:00:22:22", "name": "Bob phone 01", "presence_end": 0, "presence_start": 0, "properties": {"device_option0": "value20", "device_option1": "value21"}, "user_id": 1}, {"expire_time": 0, "id": "00:00:00:33:33:33", "name": "Bob phone 02", "presence_end": 0, "presence_start": 0, "properties": {"device_option0": "value30", "device_option1": "value31"}, "user_id": 1}, {"expire_time": NOW + 3600, "id": "00:00:00:00:00:11", "name": "Alice phone 01", "presence_end": NOW + 200, "presence_start": NOW + 500, "properties": {"device_option0": "value10", "device_option1": "value11"}, "user_id": 0}]

[{'expire_time': NOW + 3600, 'id': '00:00:00:00:00:11', 'name': 'Alice phone 01', 'presence_end': NOW + 200, 'presence_start': NOW + 500, 'properties': {'device_option0': 'value10', 'device_option1': 'value11'}, 'user_id': 0}, {'expire_time': 0, 'id': '00:00:00:00:22:22', 'name': 'Bob phone 01', 'presence_end': 0, 'presence_start': 0, 'properties': {'device_option0': 'value20', 'device_option1': 'value21'}, 'user_id': 1}, {'expire_time': 0, 'id': '00:00:00:33:33:33', 'name': 'Bob phone 02', 'presence_end': 0, 'presence_start': 0, 'properties': {'device_option0': 'value30', 'device_option1': 'value31'}, 'user_id': 1}]

class ViewsTest(unittest.TestCase):

    def setUp(self):
        self.api = api.app.test_client()
        app.config.from_object(TEST_CONFIG)
        with app.app_context():
            db.session.close()  # pylint: disable=no-member
            db.drop_all()
            db.create_all()
            alice = users.update(
                id=0,
                name='Alice',
                settings={ 'option0': 'value0', 'option1': 'value1' }
            )
            alice_device = devices.update(
                id='00:00:00:00:00:11',
                name='Alice phone 01',
                expire_time=datetime.datetime.fromtimestamp(NOW + 3600),
                presence_start=datetime.datetime.fromtimestamp(NOW + 500),
                presence_end=datetime.datetime.fromtimestamp(NOW + 200),
                properties={'device_option0': 'value10', 'device_option1': 'value11'},
                user_id=0
            )
            alice.devices.append(alice_device)
            bob = users.update(
                id=1,
                name='Bob',
                settings={ 'option0': 'value20', 'option1': 'value21' }
            )
            bob_device_1 = devices.update(
                id='00:00:00:00:22:22',
                name='Bob phone 01',
                expire_time=datetime.datetime.fromtimestamp(0),
                presence_start=datetime.datetime.fromtimestamp(0),
                presence_end=datetime.datetime.fromtimestamp(0),
                properties={'device_option0': 'value20', 'device_option1': 'value21'},
                user_id=1
            )
            bob.devices.append(bob_device_1)
            bob_device_2 = devices.update(
                id='00:00:00:33:33:33',
                name='Bob phone 02',
                expire_time=datetime.datetime.fromtimestamp(0),
                presence_start=datetime.datetime.fromtimestamp(0),
                presence_end=datetime.datetime.fromtimestamp(0),
                properties={'device_option0': 'value30', 'device_option1': 'value31'},
                user_id=1
            )
            bob.devices.append(bob_device_2)
            db.session.commit()  # pylint: disable=no-member

    def test_mac_match(self):
        res = self.api.get('/devices?id='+ACTIVE_DEVICE_RESULT)
        self.assertEqual(json.loads(res.data.decode()), ACTIVE_DEVICE_RESULT, msg="Accurately identify a MAC address")

    def test_rejects_not_mac(self):
        res = self.api.get('/devices?id=b8:27:eb:cd:cb:7Z')
        self.assertEqual(json.loads(res.data.decode()), {'message': '"b8:27:eb:cd:cb:7Z" is not a valid device ID.'}, msg='Accurately identify when not a MAC address')

    def test_rejects_missing_mac(self):
        res = self.api.get('/devices?id=DE:AD:00:00:00:00')
        self.assertEqual(json.loads(res.data.decode()), {'message': '"DE:AD:00:00:00:00" is not an existing device.'}, msg='Accurately identify when MAC address is not in the database')

    def test_list_all_devices(self):
        """Broken due to timestamp issues"""
        res = self.api.get('/devices')
        result = json.loads(res.data.decode())
        self.assertEqual(result, ALL_DEVICES_RESULT, msg="Lists all device records")

    def test_list_active_devices(self):
        """Broken probably due to comparing lists of dicts."""
        res = self.api.get('/devices?active=true')
        result = json.loads(res.data.decode())
        result.sort(key=lambda x: x['id'])
        ACTIVE_DEVICES_RESULT.sort(key=lambda x: x['id'])
        self.assertEqual(result, ACTIVE_DEVICES_RESULT, msg="Lists all active devices")

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
        """Clear out the database befor the next text."""
        with app.app_context():
            db.drop_all()
            db.session.commit()  # pylint: disable=no-member


if __name__ == '__main__':
    unittest.main()
