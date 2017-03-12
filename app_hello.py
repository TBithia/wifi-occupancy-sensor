from flask import Flask


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


if __name__ == "__main__":
    app.run()
