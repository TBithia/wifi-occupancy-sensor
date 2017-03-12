from flask import Blueprint
import json, re

mac_pattern = re.compile('^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$')

wifi_occupancy_sensor = Blueprint('wifi_occupancy_sensor',__name__)


@wifi_occupancy_sensor.route('/')
def list_active_devices():
	return json.dumps([])


@wifi_occupancy_sensor.route('/<mac>')
def show_device(mac):
	if mac_pattern.match(mac):
		# res = conn.execute("select * from present_mac where mac = '%s'"%(mac))
		res = 1
	else:
		res = 0
	return json.dumps(res) # json.dumps({})
