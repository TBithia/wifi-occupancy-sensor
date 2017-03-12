class Lease(object):
    def __init__(self, exp_ts=None, mac_address=None, ip_address=None, hostname=None):
        self.exp_ts = exp_ts
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.hostname = hostname

    def __repr__():
        return ' '.join([self.exp_ts, self.mac_address, self.ip_address, self.hostname])
