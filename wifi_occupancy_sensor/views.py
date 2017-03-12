from wifi_occupancy_sensor import app
import controllers

from flask import Response
from functools import wraps
import json
import logging
import re
import traceback

logger = logging.getLogger(__name__)

mac_pattern = re.compile('^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$')


def raw_response(body, status=200):
    return Response(
        json.dumps(body),
        status = status,
        mimetype = 'application/json')

def error_response(error, status=400):
    return raw_response(
        {'result': 'failed', 'error': error},
        status = status)

def ok_response(body={}, status=200):
    response = {'result': 'ok'}
    response.update(body)
    return raw_response(response, status=status)

def json_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger.debug(traceback.format_exc())
            return error_response(traceback.format_exc())
    return wrapper


@app.route('/')
def hello():
    '''
    Say hello, to show that the server is up and running.
    '''
    return 'Hello, World!'


@app.route('/occupancy')
@json_exception
def list_active_devices():
    '''
    List the devices that have active leases.
    '''
    return raw_response([
        lease.__dict__
        for lease in controllers.list_active_devices()
    ])


@app.route('/occupancy/<mac>')
@json_exception
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
    return raw_response(res) # json.dumps({})
