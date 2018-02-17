"""Handle the callback input from dnsmasq's `--dhcp-script`.

Arguments:
    1: The action taken: "add", "old" or "del"
    2: The MAC address of the host (or DUID for IPv6)
    3: The IP address.
    4: The hostname, if known.

Environment:
    DNSMASQ_LEASE_EXPIRES: Time the lease expires in seconds since epoc.
    DNSMASQ_TIME_REMAINING: The number of seconds until lease expires.

Notes:
    http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
    `add` means this lease has been created.
    `del` means this lease has been destroyed.
    `old` is a notification of an existing lease when dnsmasq starts, or a
    change to MAC address or hostname of an existing lease (also, lease length
    or expiry and client-id, if leasefile-ro is set).

"""

import datetime
import json
import logging
import os
import sys

# this can be set in the enviroment of the dnsmasq process
CONFIG = __import__(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])


def adjust_to_utc(timestamp):
    local_time = datetime.datetime.fromtimestamp(timestamp)
    dumby_utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    utcoffset = local_time - dumby_utc_time
    return local_time + utcoffset


class Device:

    def __init__(self, mac_address, ip_address, hostname, expire_timestamp):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.hostname = hostname
        self.expire_timestamp = expire_timestamp
        self.presence_end = None

    def delete(self):
        self.presence_end = datetime.datetime.utcnow()

    def encode(self):
        return json.dumps({
            'mac_address': self.mac_address,
            'ip_address': self.ip_address,
            'hostname': self.hostname,
            'expire_timestamp': self.expire_timestamp,
            'presence_end': self.presence_end
        }).encode()


def signal(device):
    """Send the device info somewhere."""
    pass


def dnsmasq_callback():
    action = sys.argv[1]
    if action not in ('add', 'old', 'del'):
        logger.debug('dnsmasq_callback: sys.argv = %s', sys.argv)
        selections = {
            key: value for key, value in os.environ.items()
            if 'dnsmasq' in key.lower()
        }
        logger.debug('dnsmasq_callback: selected os.environ = %s', selections)
        return None
    device = Device(sys.argv[2], sys.argv[3], sys.argv[4], os.environ['DNSMASQ_LEASE_EXPIRES'])
    if action == 'del':
        device.delete()
    signal(device)


if __name__ == '__main__':
    logger = logging.getLogger(name='wifi-occupancy-sensor-dnsmasq-callback') #  pylint: disable=invalid-name
    dnsmasq_callback()
