from wifi_occupancy_sensor import app
import json, re

mac_pattern = re.compile('^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$')

@app.route('/')
def hello():
    '''
    Say hello, to show that the server is up and running.
    '''
    return 'Hello, World!'


@app.route('/occupancy')
def list_active_devices():
    '''
    List the devices that have active leases.
    '''
    return json.dumps([])


@app.route('/occupancy/<mac>')
def show_device(mac):
    '''
    List the details of a specific device.
    (Right now, just indicates if the MAC address passes validation.)
    '''
    if mac_pattern.match(mac):
        # res = conn.execute("select * from present_mac where mac = '%s'"%(mac))
        res = 1
    else:
        res = 0
    return json.dumps(res) # json.dumps({})
