import logging
import argparse
import requests

from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import current_app
from flask import json
from flask import request

app = Flask(__name__)

auth_data=open('auth.json')
data = json.load(auth_data)
auth_data.close()
token = data['token']

crt_data=open('config.json')
data = json.load(crt_data)
crt_data.close()
crt = data['crt']
crtKey = data['crtKey']

parser = argparse.ArgumentParser(description='Selection between http and https')
parser.add_argument('-http', action='store_false', default=True,
                    dest='boolean_switch',
                    help='Set flag if you want send data through http')

results = parser.parse_args()

@app.route('/<action>/trigger', methods=['POST'])
def event_listener(action):
    from salt.utils.event import SaltEvent

    authToken = request.headers['X-AUTH-TOKEN']

    if authToken != token:
        return "X-AUTH-TOKEN is wrong"

    content = request.get_json()

    data = content['data']
    room = content['room']

    payload = { 'data' : data, 'room' : room }

    sock_dir = '/var/run/salt/minion'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, action)

    return "success"

def debug():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    if results.boolean_switch:
        app.run(host='0.0.0.0', debug=True, ssl_context=(crt, crtKey))
    else:
        app.run(host='0.0.0.0', debug=True)
