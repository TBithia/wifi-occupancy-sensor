from flask import Flask

app = Flask(__name__)

from wifi_occupancy_sensor import views
