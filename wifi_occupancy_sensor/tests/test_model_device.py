
import datetime
import unittest

from wifi_occupancy_sensor import app, db, devices

from wifi_occupancy_sensor.models.devices import Device
from wifi_occupancy_sensor.tests.testdata import TEST_CONFIG

# pylint: disable=line-too-long
ALICE_DEVICE_DICT = {
    'name': 'Alice phone 01',
    'expire_time': 0,
    'presence_start': 0,
    'presence_end': 0,
    'user_id': None,  # not adding to a user so this is None
    'id': '00:00:00:00:00:11',
    'properties': {'device_option0': 'value10', 'device_option1': 'value11'}
}

ALICE_DEVICE_PROPERTIES_DICT = {'device_option0': 'value10', 'device_option1': 'value11'}
ALICE_DEVICE_NAME = 'Alice phone 01'
ALICE_DEVICE_EXPIRE_TIME = datetime.datetime.fromtimestamp(0)
ALICE_DEVICE_PRESENCE_START = datetime.datetime.fromtimestamp(0)
ALICE_DEVICE_PRESENCE_END = datetime.datetime.fromtimestamp(0)
ALICE_DEVICE_ID = '00:00:00:00:00:11'

UPDATED_DEVICE_NAME = 'Eve\'s phone now!'
UPDATED_DEVICE_UPDATE_ADDRESS = '00:00:00:00:BE:EF'
UPDATED_DEVICE_PROPERTIES_DICT = {'device_option0': 'value10_changed', 'device_option1': 'value11_changed'}
UPDATED_DEVICE_EXPIRE_TIME = datetime.datetime.fromtimestamp(3)
UPDATED_DEVICE_PRESENCE_START = datetime.datetime.fromtimestamp(3)
UPDATED_DEVICE_PRESENCE_END = datetime.datetime.fromtimestamp(3)


class TestUser(unittest.TestCase):
    """Just testing the additional methods and not the SQLAlchemy stuff,
    for now.

    """

    def setUp(self):
        """Creates a new database for the unit test to use."""
        app.config.from_object(TEST_CONFIG)
        with app.app_context():
            db.session.close()  # pylint: disable=no-member
            db.drop_all()
            db.create_all()
            devices.update(
                id='00:00:00:00:00:11',
                name='Alice phone 01',
                expire_time=datetime.datetime.fromtimestamp(0),
                presence_start=datetime.datetime.fromtimestamp(0),
                presence_end=datetime.datetime.fromtimestamp(0),
                properties={'device_option0': 'value10', 'device_option1': 'value11'},
                user_id=0
            )
            db.session.commit()  # pylint: disable=no-member

    def test_all_set(self):
        with app.app_context():
            device = devices.query(Device).filter_by(id=ALICE_DEVICE_ID).one_or_none()
            print('DEBUG:', device.expire_time, type(device.expire_time))
            self.assertEqual(device.name, ALICE_DEVICE_NAME)
            self.assertEqual(device.expire_time, ALICE_DEVICE_EXPIRE_TIME)
            self.assertEqual(device.presence_start, ALICE_DEVICE_PRESENCE_START)
            self.assertEqual(device.presence_end, ALICE_DEVICE_PRESENCE_END)
            self.assertEqual(device.id, ALICE_DEVICE_ID)
            self.assertEqual(dict(device.properties), ALICE_DEVICE_PROPERTIES_DICT)

    def test_update_all(self):
        with app.app_context():
            device = devices.query(Device).one_or_none()
            device.update({
                'name': UPDATED_DEVICE_NAME,
                'expire_time': UPDATED_DEVICE_EXPIRE_TIME,
                'presence_start': UPDATED_DEVICE_PRESENCE_START,
                'presence_end': UPDATED_DEVICE_PRESENCE_END,
                'properties': UPDATED_DEVICE_PROPERTIES_DICT
            })
            print('DEBUG:', device.expire_time, type(device.expire_time))
            self.assertEqual(device.name, UPDATED_DEVICE_NAME)
            self.assertEqual(device.expire_time, UPDATED_DEVICE_EXPIRE_TIME)
            self.assertEqual(device.presence_start, UPDATED_DEVICE_PRESENCE_START)
            self.assertEqual(device.presence_end, UPDATED_DEVICE_PRESENCE_END)
            self.assertEqual(dict(device.properties), UPDATED_DEVICE_PROPERTIES_DICT)

    def test_update_all_and_reread(self):
        # ORM doesn't always sync up right away if the configs aren't right.
        # This should catch that.
        with app.app_context():
            device = devices.query(Device).one_or_none()
            device.update({
                'name': UPDATED_DEVICE_NAME,
                'expire_time': UPDATED_DEVICE_EXPIRE_TIME,
                'presence_start': UPDATED_DEVICE_PRESENCE_START,
                'presence_end': UPDATED_DEVICE_PRESENCE_END,
                'properties': UPDATED_DEVICE_PROPERTIES_DICT
            })
            print('DEBUG:', device.expire_time, type(device.expire_time))
            reread_device = devices.query(Device).filter_by(id=ALICE_DEVICE_ID).one_or_none()
            # reread device must be equal to the original object
            self.assertEqual(device, reread_device)
            self.assertEqual(device.name, reread_device.name)
            self.assertEqual(device.expire_time, reread_device.expire_time)
            self.assertEqual(device.presence_start, reread_device.presence_start)
            self.assertEqual(device.presence_end, reread_device.presence_end)
            self.assertEqual(device.user_id, reread_device.user_id)
            self.assertEqual(device.metadata, reread_device.metadata)

    def test_iter(self):
        with app.app_context():
            device = devices.query(Device).filter_by(id=ALICE_DEVICE_ID).one_or_none()
            print('DEBUG:', device.expire_time, type(device.expire_time))
            self.assertEqual(dict(device), ALICE_DEVICE_DICT)

    def tearDown(self):
        """Clear out the database befor the next text."""
        with app.app_context():
            db.drop_all()
            db.session.commit()  # pylint: disable=no-member


if __name__ == '__main__':
    unittest.main()

