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
import logging
import os
import sys

from wifi_occupancy_sensor.controllers import connector
from wifi_occupancy_sensor.models.devices import Devices


# this can be set in the enviroment of the dnsmasq process
CONFIG = __import__(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])


def adjust_to_utc(timestamp):
    local_time = datetime.datetime.fromtimestamp(timestamp)
    dumby_utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    utcoffset = local_time - dumby_utc_time
    return local_time + utcoffset


def dnsmasq_callback():
    devices = connector(
        CONFIG.get('SQLALCHEMY_DATABASE_URI'),
        Devices
    )
    action = sys.argv[1]
    if action not in ('add', 'old', 'del'):
        logger.debug('dnsmasq_callback: sys.argv = %s', sys.argv)
        selections = {
            key: value for key, value in os.environ.items()
            if 'dnsmasq' in key.lower()
        }
        logger.debug('dnsmasq_callback: selected os.environ = %s', selections)
        return None
    mac_address = sys.argv[2]
    ip_address = sys.argv[3]
    hostname = sys.argv[4]
    expire_timestamp = os.environ['DNSMASQ_LEASE_EXPIRES']
    device = devices.update(
        id=mac_address,
        expire_time=adjust_to_utc(expire_timestamp),
        address=ip_address,
        name=hostname
    )
    if action == 'del':
        device.presence_end = datetime.datetime.utcnow()


if __name__ == '__main__':
    logger = logging.getLogger(name='wifi-occupancy-sensor-dnsmasq-callback') #  pylint: disable=invalid-name
    dnsmasq_callback()
