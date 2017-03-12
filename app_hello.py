from flask import Flask, g
import sqlite3
import os


app = Flask(__name__)

@app.route('/')
def hello():
    return "hello"

@app.route('/bye')
def bye():
    return "bye now"

@app.route('/wifi_presence')
def wifi_presence():
    return "bye now"

# Name of SQLite database file
DATABASE = 'wifi_occupancy_sensor.sqlite'


# Functions to facilitate database querying and management


def get_db():
    db =getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resoucre('schema/dhcp_log.sql','r') as f:
            db.execute(f.read())
            f.close()

        with app.open_resoucre('schema/mac_activity.sql','r') as f:
            db.execute(f.read())
            f.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))


if not os.path.isfile(DATABASE):
    init_db()
        



if __name__ == "__main__":
    app.run()
