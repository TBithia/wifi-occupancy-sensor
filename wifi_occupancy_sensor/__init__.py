
import os

from flask import Flask, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from wifi_occupancy_sensor.controllers import database
from wifi_occupancy_sensor.models import Devices, User

SQLALCHEMY_SESSION_OPTIONS = {'autoflush': True, 'autocommit': False}

app = Flask(__name__)
app.config.from_mapping({'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'SQLALCHEMY_ECHO': True})
if os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE']:
    app.config.from_pyfile(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])

db = SQLAlchemy(app, model_class=database.Model, session_options=SQLALCHEMY_SESSION_OPTIONS)
users = database.Helper(db.session, User)
devices = Devices(db.session)

api = Api(app)
from wifi_occupancy_sensor.views import rest
api.add_resource(rest.Users, '/users')
api.add_resource(rest.Devices, '/devices')
