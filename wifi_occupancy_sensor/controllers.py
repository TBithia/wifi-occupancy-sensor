import models

LEASES_FILE = '/var/lib/misc/dnsmasq.leases'

def list_active_devices():
    '''
    Check the leases file and return the list of active devices.
    '''
    leases = []
    with open(LEASES_FILE, 'r') as leases_file:
        for line in leases_file:
            leases.append(models.Lease(*line.split(' ')[:4]))
    return leases
