#from wifi_occupancy_sensor import models

LEASES_FILE = 'wifi_occupancy_sensor/static/test/test.leases'#'/var/lib/misc/dnsmasq.leases'

def list_active_devices():
    '''
    Check the leases file and return the list of active devices.
    '''
    leases = []
    with open(LEASES_FILE, 'r') as leases_file:
        for line in leases_file:
            leases.append(line.split(' ')[:5])
            #leases.append(models.Lease(*line.split(' ')[:4]))
    return leases
