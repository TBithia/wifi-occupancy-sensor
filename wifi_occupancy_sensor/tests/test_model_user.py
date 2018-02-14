
import datetime
import unittest

from wifi_occupancy_sensor import app, db, users

from wifi_occupancy_sensor.models.users import User

TEST_ID = 0
TEST_USER_NAME = 'Alice'
TEST_SETTINGS_DICT = {'option0': 'value0', 'option1': 'value1'}
TEST_PRESENCE_START = TEST_PRESENCE_END = datetime.datetime.fromtimestamp(1)
TEST_ITER_OUTPUT = {
    'devices': [],
    'id': TEST_ID,
    'name': TEST_USER_NAME,
    'settings': TEST_SETTINGS_DICT
}


class TEST_CONFIG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class TestUser(unittest.TestCase):
    """Just testing the additional methods and not the SQLAlchemy stuff,
    for now.

    """

    def setUp(self):
        """
        Creates a new database for the unit test to use
        """
        app.config.from_object(TEST_CONFIG)
        with app.app_context():
            db.session.close()  # pylint: disable=no-member
            db.drop_all()
            db.create_all()
            users.update(
                id=TEST_ID,
                name=TEST_USER_NAME,
                settings=TEST_SETTINGS_DICT,
            )
            db.session.commit()  # pylint: disable=no-member

    def test_update_all_set(self):
        with app.app_context():
            user = users.query(User).one_or_none()
            user.update(name=TEST_USER_NAME, settings=TEST_SETTINGS_DICT)
            reread_user = users.query(User).filter_by(id=TEST_ID).one_or_none()
            self.assertEqual(user, reread_user)
            self.assertEqual(user.name, TEST_USER_NAME)
            self.assertEqual(dict(user.settings), TEST_SETTINGS_DICT)

    def test_iter(self):
        with app.app_context():
            user = users.query(User).filter_by(id=TEST_ID).one_or_none()
            self.assertEqual(dict(user), TEST_ITER_OUTPUT)

    def tearDown(self):
        """
        Ensures that the database is emptied for next unit test
        """
        with app.app_context():
            db.drop_all()
            db.session.commit()  # pylint: disable=no-member
