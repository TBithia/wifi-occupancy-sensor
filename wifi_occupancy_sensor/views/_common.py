

import datetime
import re

MAC_PATTERN = re.compile(
    '^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$'
)

def _normalize_datetime(value):
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, int):
        if value > 10**12:
            raise TypeError(
                '`value` must be a `datetime.datetime` object, or an'
                ' `int` or `str` UNIX timestamp. Got: {}'.format(value)
            )
        if value > 10**9:
            value = value / 1000
        return  datetime.datetime.fromtimestamp(value)
    if isinstance(value, str):
        original_value = value
        value = value.split('.')[0]
        if not value.isnumeric():
            raise TypeError(
                '`value` must be a `datetime.datetime` object, or an'
                ' `int` or `str` UNIX timestamp. Got: {}'.format(
                    original_value
                )
            )
        if len(value) == 13:
            value = value[:-3]
        if len(value) != 10:
            raise TypeError(
                '`value` must be a `datetime.datetime` object, or an'
                ' `int` or `str` UNIX timestamp. Got: {}'.format(
                    original_value)
            )
        return datetime.datetime.fromtimestamp(int(value))
