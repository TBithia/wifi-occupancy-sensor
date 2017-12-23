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


import logging
import os
import sys

from wifi_occupancy_sensor.controllers import leases, database

# this can be set in the enviroment of the dnsmasq process
CONFIG = __import__(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])


def _dnsmasq_callback():
    lease_db = database.get_table(leases.get_leases(CONFIG), CONFIG)
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
    exp_ts = os.environ['DNSMASQ_LEASE_EXPIRES']
    func = {
        'add': lease_db.update,
        'del': lease_db.pop,
        'old': lease_db.update
        }.get(action)
    func(
        exp_ts=exp_ts,
        mac_address=mac_address,
        ip_address=ip_address,
        hostname=hostname
    )


if __name__ == '__main__':
    logger = logging.getLogger(name='wifi-occupancy-sensor-dnsmasq-callback') #  pylint: disable=invalid-name
    _dnsmasq_callback()
