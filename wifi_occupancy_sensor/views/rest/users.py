
import re
from datetime import datetime as dt

from flask_restful import abort, Api, reqparse, Resource

from wifi_occupancy_sensor import app, api, db, devices, users
from wifi_occupancy_sensor.views.rest._common import gen_parser


class Users(Resource):

    parser = gen_parser(
        {'name': 'id', 'type': int},
        {'name': 'name', 'type': str},
        {'name': 'settings', 'type': dict, 'location': 'json'}
    )

    def get(self):
        args = self.parser.parse_args()
        if not args.id:
            return [dict(x) for x in users.find_all()]
        user = users.find(id=args.id)
        if not user:
            abort(404, message='User not found')
        return dict(user)

    def post(self):
        args = self.parser.parse_args()
        if not args.name:
            abort(400, message='The `name` parameter is required')
        spec = {'name': args.name}
        if args.id:
            spec['id'] = args.id
        if args.settings:
            spec['settings'] = args.settings
        user = users.update(id=args.id, settings=args.settings)
        return {'id': user.id}
