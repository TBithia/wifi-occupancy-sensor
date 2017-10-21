
import os
import sqlite3


def get_table(table_class, config):
    db = DB(config.DATABASE_FILENAME)
    return table_class(db)


def _make_dict(cursor, row):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}


def _where(where):
    where_parts = []
    values = []
    for key, value in where.items():
        where_parts.append('%s=?' % key)
        values.append(value)
    return ','.join(where_parts), values


class DB:

    def __init__(self, config, *tables):
        self._filename = config.get('DATABASE_FILENAME')
        init_db = not os.path.isfile(self._filename)
        self._conn = sqlite3.connect(self._filename)
        self._conn.row_factory = _make_dict
        if init_db:
            for table in tables:
                self.load(table.schema)

    def load(self, schema):
        self._conn.execute(schema)

    def close(self):
        if self._conn:
            self._conn.close()

    def insert(self, table, row_dict):
        columns = list(row_dict.items())
        columns.sort(key=lambda x: x[0])
        keys = [x[0] for x in columns]
        values = [x[1] for x in columns]
        value_format = ','.join(['?'] * len(keys))
        key_format = ','.join(keys)
        query = 'INSERT OR REPLACE INTO %s(%s) VALUES(%s)' % (
            table, key_format, value_format
        )
        self._conn.execute(query, values)

    def select(self, table, **where):
        query_parts = ['SELECT * FROM %s' % table]
        keys, values = _where(where)
        if keys:
            query_parts.append('WHERE')
            query_parts.append(keys)
        query = ' '.join(query_parts)
        return self._conn.execute(query, values).fetchall()

    def pick(self, table, where_string, *values):
        query = 'SELECT * FROM %s WHERE %s' % (table, where_string)
        return self._conn.execute(query, values).fetchall()

    def delete(self, table, **where):
        if not where:
            raise TypeError()
        query = 'DELETE FROM %s WHERE ' %  table
        keys, values = _where(where)
        self._conn.execute(query+keys, values)


class Table:

    name = None
    record_class = None
    schema = 'CREATE TABLE IF NOT EXISTS %s ( %s )'

    def __init__(self, db):
        self.db = db
        self.db.load(self.schema)

    def get(self, **where):
        records = self.db.select(self.name, **where)
        return [self.record_class(**record) for record in records]

    def pick(self, where_string, *values):
        return self.db.pick(self.name, where_string, *values)

    def update(self, records):
        for record in records:
            self.db.insert(self.name, **dict(record))

    def pop(self, **where):
        records = self.get(**where)
        self.db.delete(**where)
        return records
