from flask import Blueprint
import json, re

mac_pattern = re.compile('^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$')

wifi_presence = Blueprint('wifi_presence',__name__)


@wifi_presence.route('/')
def list_active_devices():
	return json.dumps([])


@wifi_presence.route('/<mac>')
def show_device(mac):
	if mac_pattern.match(mac):
		# res = conn.execute("select * from present_mac where mac = '%s'"%(mac))
		res = 1
	else:
		res = 0
	return json.dumps(res) # json.dumps({})