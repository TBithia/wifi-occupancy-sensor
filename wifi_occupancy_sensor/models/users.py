
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.orm import relationship

from wifi_occupancy_sensor.controllers import database


class SettingsItem(database.ItemMixin, database.Model):

    __tablename__ = 'users__dict__settings'

    key_type = Text
    value_type = Text
    parent_id_column = 'users.id'


class UserSettings(database.DictProxy):

    childclass = SettingsItem


class User(database.Model):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    devices = relationship(
        'Device',
        cascade='all, delete-orphan'
    )

    _settings = relationship(
        'SettingsItem',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def settings(self):
        return UserSettings(self, '_settings')

    def update(self, **spec):
        self.name = spec.get('name', self.name)
        self.settings.update(spec.get('settings', {}))

    def __iter__(self):
        return iter((
            ('id', self.id),
            ('name', self.name),
            ('devices', list(self.devices or [])),
            ('settings', dict(self.settings or {}))
        ))
