
import os

from flask import Flask, g
from flask_restful import Api

from wifi_occupancy_sensor.controllers import DB, Devices, Users

app = Flask(__name__)
app.config.from_pyfile(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DB(app.config, Devices, Users)
    return db


def devices():
    return Devices(get_db())


def users():
    return Users(get_db())


from wifi_occupancy_sensor.views import rest
api.add_resource(rest.Users, '/users')
api.add_resource(rest.Devices, '/devices')

