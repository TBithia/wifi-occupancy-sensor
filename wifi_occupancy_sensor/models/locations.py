"""This models the physical locations defined by the user.

Each location is defined by a polygon of points. Each point is defined by a set
of signal measurements. Each signal measurement is composed of a reference to a
source device and the signal level measurement taken by that source device.

There are two methods of translating signal measurements into physical
locations.
* The first uses a single source device and relies on a unique set of signal
levels from a given location.
  * The user is in room A and the source device measures signal level X.
  When the user returns to the location the source device sees roughly signal
  level X and concludes that the user is in room A.
* The second method is plain old triangulation and requires two or more source
devices.

"""

from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from wifi_occupancy_sensor.controllers import Model


class Location(Model):

    __tablename__ = 'locations'

    id = Column(Text, primary_key=True, unique=True)
    points = relationship(
        'Point',
        cascade='all, delete-orphan'
    )

class Point(Model):

    __tablename__ = 'locations__points'

    id = Column(Text, primary_key=True, unique=True)
    position = Column(Integer, unique=True)
    signals = relationship(
        'Signal',
        cascade='all, delete-orphan'
    )


class Signal(Model):

    __tablename__ = 'locations__points__signals'

    id = Column(Text, primary_key=True, unique=True)
    strength = Column(Integer)
    source = relationship(
        'SourceDevice',
        collection_map_class=attribute_mapped_collection('source_devices.id'),
        cascade='all, delete-orphan'
    )

    def __iter__(self):
        return iter((('strength', self.strength), ('source_id', self.source.id)))
