
import datetime
import os
import unittest

from wifi_occupancy_sensor import app, db, users

from wifi_occupancy_sensor.models.users import User
from wifi_occupancy_sensor.tests.testdata import TEST_CONFIG


# pylint: disable=line-too-long

ALICE_ID = 0
ALICE_USER_NAME = 'Alice'
ALICE_SETTINGS_DICT = {'option0': 'value0', 'option1': 'value1'}
ALICE_DICT = {
    'devices': [],
    'id': 0,
    'name': 'Alice',
    'settings': {'option0': 'value0', 'option1': 'value1'}
}

UPDATED_SETTINGS_DICT = {'option0': 'value10', 'option1': 'value11'}
UPDATED_USER_NAME = 'Eve'


class TestUser(unittest.TestCase):
    """Just testing the additional methods and not the SQLAlchemy stuff,
    for now.

    """

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        with app.app_context():
            db.session.close()  # pylint: disable=no-member
            db.drop_all()
            db.create_all()
            alice = users.update(
                id=0,
                name='Alice',
                settings={ 'option0': 'value0', 'option1': 'value1' }
            )
            db.session.commit()  # pylint: disable=no-member

    def test_all_set(self):
        with app.app_context():
            user = users.query(User).one_or_none()
            self.assertEqual(user.id, ALICE_ID)
            self.assertEqual(user.name, ALICE_USER_NAME)
            self.assertEqual(dict(user.settings), ALICE_SETTINGS_DICT)

    def test_update_all(self):
        with app.app_context():
            user = users.query(User).one_or_none()
            user.update({'name': UPDATED_USER_NAME, 'settings': UPDATED_SETTINGS_DICT})
            self.assertEqual(user.name, UPDATED_USER_NAME)
            self.assertEqual(dict(user.settings), UPDATED_SETTINGS_DICT)

    def test_update_all_reread(self):
        with app.app_context():
            user = users.query(User).one_or_none()
            user.update({'name': UPDATED_USER_NAME, 'settings': UPDATED_SETTINGS_DICT})
            reread_user = users.query(User).filter_by(id=ALICE_ID).one_or_none()
            self.assertEqual(user, reread_user)

    def test_iter(self):
        with app.app_context():
            user = users.query(User).filter_by(id=ALICE_ID).one_or_none()
            self.assertEqual(dict(user), ALICE_DICT)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        with app.app_context():
            db.drop_all()
            db.session.commit()  # pylint: disable=no-member


if __name__ == '__main__':
    unittest.main()

