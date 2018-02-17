
from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Integer, Text, ForeignKey, inspect
from sqlalchemy.orm import relationship, reconstructor

from wifi_occupancy_sensor.controllers.database import and_, ItemMixin, DictProxy, Helper, Model, or_


class Device(Model):
    """

    Attributes:
        id (str): Device ID. MAC or other device specific UUID.
        name (str): The hostname or other self advertised human readable device name.
        expire_time (datetime.datetime): The time the DHCP lease expires.
        presence_start (datetime.datetime): The time the device was first detected.
        presence_end (datetime.datetime): The time the device was last determined to have left the system.
        active (bool): True if the device matches the criteria for being present.
        expired (bool): True if `expire_time` is older than now.
        properties (DeviceMetaData): Arbitrary metadata about the device.

    """

    __tablename__ = 'devices'

    id = Column(Text, primary_key=True, unique=True)
    name = Column(Text)
    expire_time = Column(DateTime)
    presence_start = Column(DateTime)
    presence_end = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    _device_metadata = relationship(
        'DeviceMetaDataItem',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def properties(self):
        return DeviceMetaData(self, '_device_metadata')

    def update(self, spec):
        """Update ``Device`` attributes if they are provided by name in ``spec``.

        Keyword Arguments:
            name (str):
            expire_time (datetime.datetime):
            presence_start (datetime.datetime):
            presence_end (datetime.datetime):
            properties (dict):

        """
        if isinstance(spec, Device) and not inspect(spec).detached:
            # this assumes the Device object is both attached and newly
            # instantiated
            spec = dict(spec)
        if not self.id and spec.get('id'):
            self.id = spec.get('id', self.id)
        if not self.user_id and spec.get('user_id'):
            self.user_id = spec.get('user_id')
        self.name = spec.get('name', self.name)
        self.expire_time = spec.get('expire_time', self.expire_time)
        self.presence_start = spec.get('presence_start', self.presence_start)
        self.presence_end = spec.get('presence_end', self.presence_end)
        self.properties.update(spec.get('properties', {}))

    @property
    def active(self):
        now = dt.utcnow()
        return (self.expire_time > now and
                self.presence_end < self.presence_start and
                self.presence_start < now)

    @property
    def expired(self):
        now = dt.utcnow()
        return self.expire_time <= now

    def __iter__(self):
        return iter((
            ('id', self.id),
            ('name', self.name),
            ('expire_time', self.expire_time.timestamp() if self.expire_time else None),
            ('presence_start', self.presence_start.timestamp() if self.presence_start else None),
            ('presence_end', self.presence_end.timestamp() if self.expire_time else None),
            ('user_id', self.user_id),
            ('properties', dict(self.properties))
        ))

class DeviceMetaDataItem(ItemMixin, Model):

    __tablename__ = 'devices__dict__metadata'

    key_type = Text
    value_type = Text
    parent_id_column = Device.__tablename__+'.id'


class DeviceMetaData(DictProxy):

    childclass = DeviceMetaDataItem


class Devices(Helper):

    datatype = Device

    @property
    def active(self):
        now = dt.utcnow()
        return self.query(Device).filter(
            and_(
                Device.expire_time > now,
                Device.presence_end < Device.presence_start,
                Device.presence_start < now
            )
        ).all()

    @property
    def inactive(self):
        now = dt.utcnow()
        return self.query(Device).filter(
            or_(
                Device.expire_time <= now,
                Device.presence_end > Device.presence_start,
                Device.presence_start > now
            )
        ).all()
