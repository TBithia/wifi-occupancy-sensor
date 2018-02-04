
import re
from datetime import datetime as dt

from flask_restful import abort, Api, reqparse, Resource

from wifi_occupancy_sensor import app, api, db, devices, users
from wifi_occupancy_sensor.models import Device
from wifi_occupancy_sensor.views._common import MAC_PATTERN, _normalize_datetime
from wifi_occupancy_sensor.views.rest._common import gen_parser


class Devices(Resource):

    parser = gen_parser(
        {'name': 'id', 'type': str},
        {'name': 'active', 'type': bool, 'default': None},
        {'name': 'signal', 'type': int},
        {'name': 'source_id', 'type': int},
        {'name': 'name', 'type': str},
        {'name': 'address', 'type': str},
        {'name': 'expire_time', 'type': int},
        {'name': 'presence_start', 'type': int},
        {'name': 'presence_end', 'type': int}
    )

    def get(self):
        args = self.parser.parse_args()
        if args.id:
            if not MAC_PATTERN.match(args.id):
                abort(400, message='"%s" is not a valid device ID.' % args.id)
            device = devices.find(id=args.id)
            if device:
                return dict(device)
            else:
                abort(400, message='"%s" is not an existing device.' %
                      device_id)
        elif args.active is True:
            active_devices = devices.active
            app.logger.debug(active_devices)
            return [dict(d) for d in active_devices]
        elif args.active is False:
            inactive_devices = devices.inactive
            app.logger.debug(inactive_devices)
            return [dict(d) for d in inactive_devices]
        return [dict(d) for d in devices.find_all()]

    def post(self):
        presence_start = presence_end = None
        args = self.parser.parse_args()
        if not args.id:
            abort(400, message='The `id` parameter is required')
        devices.update(
            id=args.id,
            name=args.name,
            user_id=args.user,
            address=args.address,
            expire_time=_normalize_datetime(args.expire_time),
            presence_start=_normalize_datetime(presence_start),
            presence_end=_normalize_datetime(presence_end)
        )

    def put(self):
        presence_start = presence_end = None
        args = self.parser.parse_args()
        if not args.id:
            abort(400, message='The `id` parameter is required')
        device = devices.find(id=args.id)
        if not device:
            abort(404, message='The device "%s" does not exist' % args.id)
        device.update(
            id=args.id,
            name=args.name,
            user_id=args.user,
            address=args.address,
            expire_time=args.expire_time,
            presence_start=presence_start,
            presence_end=presence_end
        )
