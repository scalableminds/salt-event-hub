import logging
import argparse
import sys

from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import json
from flask import request

app = Flask(__name__)

try:
    config_data = open('config.json')
except IOError:
    sys.exit("Error: can\'t find config.json")
else:
    try:
        data   = json.load(config_data)
        token  = data['token']
        crt    = data['crt']
        crtKey = data['crtKey']
    except Exception:
        sys.exit("Error: can\'t read data from config.json")
    finally:
        config_data.close()

parser = argparse.ArgumentParser(description='Selection between http and https')
parser.add_argument('--https', action='store_false', default=True,
                    dest='use_https',
                    help='Set flag if you want send data through https')

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

    if protocol.use_https:
        app.run(host='0.0.0.0', debug=True)
    else:
        app.run(host='0.0.0.0', debug=True, ssl_context=(crt, crtKey))
