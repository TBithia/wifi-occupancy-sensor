
from wifi_occupancy_sensor.controllers import database
from wifi_occupancy_sensor import models


class Devices(database.Table):

    name = 'devices'
    record_class = models.Device
    schema = database.Table.schema % ('devices', 'id TEXT PRIMARY KEY NOT NULL, user_id INTEGER, address TEXT, expire_time INTEGER, presence_start INTEGER, presence_end INTEGER')
