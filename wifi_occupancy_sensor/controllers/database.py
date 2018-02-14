
import logging

from sqlalchemy import and_, create_engine, Column, Integer, ForeignKey, or_
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists


Model = declarative_base()  # pylint: disable=invalid-name


class Helper:

    datatype = None

    def __init__(self, db_session, datatype=None):
        self.log = logging.getLogger(name=self.__class__.__name__)
        self._session = db_session
        self.datatype = datatype or self.datatype

    def flush(self):
        if self._session.dirty:
            self._session.flush()

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def find(self, **attrs):
        return self._session.query(self.datatype).filter_by(**attrs).one_or_none()

    def find_all(self, **attrs):
        return self._session.query(self.datatype).filter_by(**attrs).all()

    def update(self, **spec):
        """UPSERT"""
        spec = {key: value for key, value in spec.items() if value is not None}
        query = self.query(self.datatype)
        found = query.filter(self.datatype.id == spec.get('id')).one_or_none()
        if found:
            found.update(spec)
            return found
        else:
            return self.add(**spec)

    def add(self, **spec):
        data = self._session.merge(self.datatype(id=spec.get('id')))
        data.update(**spec)
        self._session.add(data)
        return data

    def remove(self, data):
        if isinstance(data, int):
            # data is a record id
            found = self.find(id=data)
            if found:
                self._session.delete(found)
        else:
            # data must be an instance of self.datatype
            self._session.delete(data)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._session.flush()
        self._session.close()
        return False

    def __contains__(self, url):
        condition = exists().where(self.datatype.url == url)
        found = self._session.query(self.datatype.url).filter(condition)
        if found:
            return True
        return False

    def __iter__(self):
        self._session.commit()
        self.log.debug('Dumping db to a list.')
        return iter(self._session.query(self.datatype).all())


class ItemMixin:

    item_id = Column(Integer, primary_key=True, unique=True)
    # potentially automatically cast the value via the proxy
    # hydrate_type = Column(Enum)

    @declared_attr
    def dict_key(cls):  # pylint: disable=no-self-argument, method-hidden
        return Column(cls.key_type)

    @declared_attr
    def value(cls):  # pylint: disable=no-self-argument, method-hidden
        return Column(cls.value_type)

    @declared_attr
    def parent_id(cls):  # pylint: disable=no-self-argument
        return Column(
            Integer,
            ForeignKey(cls.parent_id_column),
            nullable=False
        )

    def __init__(self, key, value):
        self.dict_key = key
        self.value = value


class DictProxy:

    keyname = 'dict_key'
    childclass = object

    def __init__(self, parent, collection_name):
        self.parent = parent
        self.collection_name = collection_name
        self.collection.autoflush(True)

    @property
    def collection(self):
        return getattr(self.parent, self.collection_name)

    def keys(self):
        descriptor = getattr(self.childclass, self.keyname)
        return [x[0] for x in self.collection.values(descriptor)]

    def __get_raw_item(self, key):
        item = self.collection.filter_by(**{self.keyname:key}).first()
        if item:
            return item
        else:
            raise KeyError(key)

    def __getitem__(self, key):
        return self.__get_raw_item(key).value

    def __setitem__(self, key, value):
        try:
            existing = self.__get_raw_item(key)
            self.collection.remove(existing)
        except KeyError:
            pass
        if not isinstance(value, self.childclass):
            value = self.childclass(key, value)
        self.collection.append(value)

    def pop(self, key):
        dict_item = self[key]
        value = dict_item.value
        self.collection.remove(dict_item)
        return value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, new_dict):
        for key, value in new_dict.items():
            if key and value:
                self[key] = value

    def __iter__(self):
        return iter(tuple((x.key, x.value) for x in self.collection))
