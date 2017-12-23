
from wifi_occupancy_sensor.controllers import database
from wifi_occupancy_sensor import models


class Users(database.Table):

    name = 'users'
    record_class = models.User
    schema = database.Table.schema % ('users', 'id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL')
