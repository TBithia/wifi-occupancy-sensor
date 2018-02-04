
import os

from flask import Flask, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from wifi_occupancy_sensor.controllers import database
from wifi_occupancy_sensor.models import Devices, User


app = Flask(__name__)
app.config.from_pyfile(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])
api = Api(app)
db = SQLAlchemy(app, model_class=database.Model)
users = database.Helper(db.session, User)
devices = Devices(db.session)

from wifi_occupancy_sensor.views import rest
api.add_resource(rest.Users, '/users')
api.add_resource(rest.Devices, '/devices')
