
import time


class User:

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __iter__(self):
        return iter((('id', self.id), ('name', self.name)))


class Device:

    def __init__(self, id=None, name=None, user_id=None, address=None, expire_time=None,
                 presence_start=None, presence_end=None):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.address = address
        self.expire_time = expire_time
        self.presence_start = presence_start
        self.presence_end = presence_end

    @property
    def present(self):
        return self.presence_end < self.presence_start and self.expire_time > time.time()

    def update(self, **values):
        for key, value in values:
            if value is None:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

    def __iter__(self):
        return iter((
            ('id', self.id),
            ('name', self.name),
            ('user_id', self.user_id),
            ('address', self.address),
            ('expire_time', self.expire_time),
            ('presence_start', self.presence_start),
            ('presence_end', self.presence_end)
        ))
