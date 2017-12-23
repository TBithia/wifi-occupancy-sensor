
import re
import time

from flask_restful import abort, Api, reqparse, Resource

from wifi_occupancy_sensor import app, api, devices, users
from wifi_occupancy_sensor.models import Device, User
from wifi_occupancy_sensor.views._common import MAC_PATTERN


def gen_parser(*args):
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(**arg)
    return parser


class Users(Resource):

    parser = gen_parser({'name': 'id', 'type': int})

    def get(self):
        args = self.parser.parse_args()
        if not args.id:
            return self.list_all_users()
        user = users().get(args.id)
        user_devices = [dict(x) for x in devices().get(user_id=user.id)]
        return dict(user)+{'devices': user_devices}

    def post(self):
        args = self.parser.parse_args()
        if not args.name:
            abort(400, message='The `name` parameter is required')
        users().update(User(name=args.name))
        return {'id': users().get(name=args.name).id}

    def list_all_users(self):
        output = []
        devs = devices()
        for user in users().get():
            output.append(dict(user) + {'devices': [dict(x) for x in devs.get(user_id=user.id)]})
        return output


class Devices(Resource):

    parser = gen_parser({'name': 'id', 'type': str}, {'name': 'active', 'type': bool, 'default': None})

    def get(self):
        args = self.parser.parse_args()
        output = []
        if args.id:
            output = self.get_device(args.id, args.active)
        elif args.active:
            output = self.list_active_devices()
        return [dict(x) for x in  output or self.list_all_devices()]

    def post(self):
        presence_start = presence_end = None
        args = self.parser.parse_args()
        if not args.id:
            abort(400, message='The `id` parameter is required')
        device = Device(id=args.id, name=args.name, user_id=args.user,
                        address=args.address, expire_time=args.expire_time,
                        presence_start=presence_start,
                        presence_end=presence_end)
        devices().update(device)

    def put(self):
        presence_start = presence_end = None
        args = self.parser.parse_args()
        if not args.id:
            abort(400, message='The `id` parameter is required')
        device = devices().get(id=args.id)
        if not device:
            abort(404, message='The device "%s" does not exist' % args.id)
        device.update(id=args.id, name=args.name, user_id=args.user,
                      address=args.address, expire_time=args.expire_time,
                      presence_start=presence_start,
                      presence_end=presence_end)
        devices().update(device)

    def list_all_devices(self):
        """List all known devices."""
        app.logger.debug(devices().get())
        devs = devices().get()
        return devs

    def list_active_devices(self):
        """List the devices that have active leases."""
        active_devices = devices().pick('presence_end < presence_start AND expire_time > ?', int(time.time()))
        app.logger.debug(active_devices)
        return active_devices

    def get_device(self, device_id, active=None):
        """List the details of a specific device."""
        if not MAC_PATTERN.match(device_id):
            abort(400, message='"%s" is not a valid device ID.' % device_id)
        devs = devices().get(id=device_id)
        if not devs:
            abort(400, message='"%s" is not an existing device.' % device_id)
        if active:
            return [x for x in devs if x.present]
        if active is False:
            return [x for x in devs if not x.present]
        return devs
