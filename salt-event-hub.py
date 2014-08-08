import logging
import argparse
import sys

from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import json
from flask import request
from flask import abort
from flask import Response

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    config_data = open('config.json')
except IOError:
    sys.exit("Error: can\'t find config.json")
else:
    try:
        data   = json.load(config_data)
        token  = data['x_auth_token']
        crt    = data['crt']
        crtKey = data['crtKey']
    except Exception:
        sys.exit("Error: can\'t read data from config.json")
    finally:
        config_data.close()

parser = argparse.ArgumentParser(description='Selection between http and https')
parser.add_argument('--https', action='store_false', default=True,
                    dest='use_https',
                    help='Set args if you want send data through https')
parser.add_argument('--host')
parser.add_argument('--port')
args = parser.parse_args()
logger.debug(args)

@app.route('/<action>/trigger', methods=['POST'])
def event_listener(action):
    from salt.utils.event import SaltEvent

    authToken = request.headers['X-AUTH-TOKEN']
    if authToken != token:
        abort(401)

    content = request.get_json()
    payload = { 'data' : content['data'], 'source' : content['source'] }

    sock_dir = '/var/run/salt/minion'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, action)

    return "OK"

@app.errorhandler(401)
def custom_401(error):
    return Response('Wrong X-AUTH-TOKEN', 401, {'HUBOTAuthenticate':'Basic realm="Proper Token Required"'})

if __name__ == '__main__':
    host = args.host if args.host else 'localhost'
    port = int(args.port) if args.port else 5000
    if args.use_https:
        app.run(host=host, port=port, debug=True)
    else:
        app.run(host=host, port=port, debug=True, ssl_context=(crt, crtKey))
