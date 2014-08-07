import logging
import argparse

from logging.handlers import RotatingFileHandler
from flask import Flask
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

protocol = parser.parse_args()

@app.route('/<action>/trigger', methods=['POST'])
def event_listener(action):
    from salt.utils.event import SaltEvent

    authToken = request.headers['X-AUTH-TOKEN']
    if authToken != token:
        return "X-AUTH-TOKEN is wrong"

    content = request.get_json()
    payload = { 'data' : content['data'], 'room' : content['room'] }

    sock_dir = '/var/run/salt/minion'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, action)

    return "success"

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    if protocol.boolean_switch:
        app.run(host='0.0.0.0', debug=True, ssl_context=(crt, crtKey))
    else:
        app.run(host='0.0.0.0', debug=True)
