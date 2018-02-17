
import datetime

# pylint: disable=line-too-long


class TEST_CONFIG:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/unittest.db'


class __User:
    """Taken from test_model_user.py"""

    user_id = None
    name = None
    settings = {}
    devices = []

    constructor_template = '''\
{self.name_lower} = users.update(
    id={self.user_id},
    name='{self.name}',
    settings={settings}
)
{devices}
'''

    request_result_template = '''\
{{
    'devices': {devices},
    'id': {self.user_id},
    'name': '{self.name}',
    'settings': {self.settings}
}}
'''

    iter_output_template = '''\
{{
    'devices': {devices},
    'id': {self.user_id},
    'name': '{self.name}',
    'settings': {self.settings}
}}
'''

    def __init__(self, devices=[]):
        self.devices = devices
        self.name_lower = self.name.lower()

    @property
    def request_result(self):
        return self.request_result_template.format(
            self=self,
            devices='[{}]'.format(', '.join(x.request_result for x in self.devices))
        )

    @property
    def constructor(self):
        settings = '{{ {} }}'.format(
                ', '.join('\'{}\': \'{}\''.format(k, v) for k, v in self.settings.items())
            )
        devices = '\n'.join(x.constructor for x in self.devices)
        return self.constructor_template.format(self=self, settings=settings, devices=devices)

    @property
    def iter_output(self):
        devices = '[{}]'.format(', '.join(x.iter_output for x in self.devices))
        return self.iter_output_template.format(self=self, devices=devices)

    def __repr__(self):
        return '''\
{self.constructor}
{self.name_lower}_rest_api_result = {self.request_result}
{self.name_lower}_dict = {self.iter_output}
{self.name_lower}_settings_dict = {self.settings}
{self.name_lower}_user_id = {self.user_id}
{self.name_lower}_user_name = '{self.name}'
'''.format(self=self)


class __Device:

    device_name = None
    device_id = None
    user_id = None
    user_name = None
    properties = None
    expire_time_timestamp = 0
    presence_start_timestamp = 0
    presence_end_timestamp = 0
    constructor_template = '''\
{self.user_name}_device = devices.update(
    id='{self.device_id}',
    name='{self.device_name}',
    expire_time={expire_time},
    presence_start={presence_start},
    presence_end={presence_end},
    properties={self.properties},
    user_id={self.user_id}
)
{self.user_name}.devices.append({self.user_name}_device)
'''

    request_result_template = '''\
{{
    'name': '{self.device_name}',
    'expire_time': {self.expire_time_timestamp},
    'presence_start': {self.presence_start_timestamp},
    'presence_end': {self.presence_end_timestamp},
    'user_id': {self.user_id},
    'id': '{self.device_id}',
    'properties': {self.properties}
}}
'''

    iter_output_template = '''\
{{
    'name': '{self.device_name}',
    'expire_time': {expire_time},
    'presence_start': {presence_start},
    'presence_end': {presence_end},
    'user_id': {self.user_id},
    'id': '{self.device_id}',
    'properties': {self.properties}
}}
'''

    def __init__(self,
                 user=None,
                 device_name = None,
                 device_id = None,
                 user_id = None,
                 user_name = None,
                 properties = None,
                 expire_time_timestamp = None,
                 presence_start_timestamp = None,
                 presence_end_timestamp = None
                 ):
        if user_id is not None:
            if isinstance(user_id, int):
                self.user_id = user_id
        if user:
            self.user_id = user.user_id
            self.user_name = user.name
        else:
            self.user_id = user_id or self.user_id
        self.device_name = device_name or self.device_name
        self.device_id = device_id or self.device_id
        self.user_name = user_name or self.user_name
        self.user_name = str(self.user_name).lower()
        self.properties = properties or self.properties
        self.expire_time_timestamp = expire_time_timestamp or self.expire_time_timestamp
        self.presence_start_timestamp = presence_start_timestamp or self.presence_start_timestamp
        self.presence_end_timestamp = presence_end_timestamp or self.presence_end_timestamp

    @property
    def constructor(self):
        return self.constructor_template.format(
            self=self,
            expire_time='datetime.datetime.fromtimestamp({})'.format(self.expire_time_timestamp),
            presence_start='datetime.datetime.fromtimestamp({})'.format(self.presence_start_timestamp),
            presence_end='datetime.datetime.fromtimestamp({})'.format(self.presence_start_timestamp)
        )

    @property
    def request_result(self):
        return self.request_result_template.format(self=self)

    @property
    def iter_output(self):
        return self.iter_output_template.format(
            self=self,
            expire_time='datetime.datetime.fromtimestamp({})'.format(self.expire_time_timestamp),
            presence_start='datetime.datetime.fromtimestamp({})'.format(self.presence_start_timestamp),
            presence_end='datetime.datetime.fromtimestamp({})'.format(self.presence_start_timestamp)
        )

    def __repr__(self):
        return '''\
{self.constructor}
{self.user_name}_device_rest_api_result = {self.request_result}
{self.user_name}_device_dict = {self.iter_output}
{self.user_name}_device_properties_dict = {self.properties}
{self.user_name}_device_name = '{self.device_name}'
{self.user_name}_device_expire_time = {expire_time}
{self.user_name}_device_expire_time_timestamp = {self.expire_time_timestamp}
{self.user_name}_device_presence_start = {presence_start}
{self.user_name}_device_presence_start_timestamp = {self.presence_start_timestamp}
{self.user_name}_device_presence_end = {presence_end}
{self.user_name}_device_presence_end_timestamp = {self.presence_end_timestamp}
{self.user_name}_device_id = '{self.device_id}'
'''.format(
        self=self,
        expire_time='datetime.datetime.fromtimestamp({})'.format(self.expire_time_timestamp),
        presence_start='datetime.datetime.fromtimestamp({})'.format(self.presence_start_timestamp),
        presence_end='datetime.datetime.fromtimestamp({})'.format(self.presence_start_timestamp)
    )

        return '''\
{self.constructor}
{self.name_lower}_rest_api_result = {self.request_result}
{self.name_lower}_dict = {self.iter_output}
{self.name_lower}_settings_dict = {self.settings}
{self.name_lower}_user_id = {self.user_id}
{self.name_lower}_user_name = '{self.name}'
'''.format(self=self)

class Alice(__User):
    """Taken from test_model_user.py"""
    user_id = 0
    name = 'Alice'
    settings = {'option0': 'value0', 'option1': 'value1'}


class AliceDevice1(__Device):
    """Alice's only device."""
    device_name = 'Alice phone 01'
    device_id = '00:00:00:00:00:11'
    user_id = Alice.user_id
    user_name = Alice.name.lower()
    properties = {'device_option0': 'value10', 'device_option1': 'value11'}

Alice.devices.append(AliceDevice1())

class Bob(__User):
    """Taken from test_model_user.py"""
    user_id = 1
    name = 'Bob'
    settings = {'option0': 'value20', 'option1': 'value21'}


class BobDevice1(__Device):
    """First device owned by Bob."""
    device_name = 'Bob phone 01'
    device_id = '00:00:00:00:22:22'
    user_id = Bob.user_id
    properties = {'device_option0': 'value20', 'device_option1': 'value21'}


class BobDevice2(__Device):
    """Second device owned by Bob."""
    device_name = 'Bob phone 02'
    device_id = '00:00:00:33:33:33'
    user_id = Bob.user_id
    properties = {'device_option0': 'value30', 'device_option1': 'value31'}


Bob.devices.append(BobDevice1())
Bob.devices.append(BobDevice2())


