
import os

from flask import Flask, g


app = Flask(__name__)  # pylint: disable=invalid-name
app.config.from_pyfile(os.environ['WIFI_OCCUPANCY_SENSOR_CONFIGFILE'])


@app.route('/')
def hello():
    return "hello"

@app.route('/bye')
def bye():
    return "bye now"

@app.route('/wifi_presence')
def wifi_presence():
    return "bye now"


'''
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DB(app.config)
    return db
'''

@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run()
