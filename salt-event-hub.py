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

parser = argparse.ArgumentParser(description='Selection between http and https')
parser.add_argument('--https', action='store_true', default=False,
                    dest='use_https',
                    help='Set args if you want send data through https')
parser.add_argument('--host', default="localhost")
parser.add_argument('--port', default=5000)
args = parser.parse_args()
logger.debug(args)

@app.route('/<action>/trigger', methods=['POST'])
def event_listener(action):
    from salt.utils.event import SaltEvent

    authToken = request.headers['X-AUTH-TOKEN']
    if args.use_https and authToken != readFromConfig('x_auth_token'):
        abort(401)

    content = request.get_json()
    payload = { 'data' : content['data'], 'source' : content['source'] }

    sock_dir = '/var/run/salt/master'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, action)

    return "OK"

@app.errorhandler(401)
def custom_401(error):
    return Response('Wrong X-AUTH-TOKEN', 401, {'Authenticate':'Basic realm="Proper Token Required"'})

def readFromConfig(key):
  try:
      config_data = open('config.json')
  except IOError:
      sys.exit("Error: can\'t find config.json")
  else:
      try:
          data   = json.load(config_data)
          value  = data[key]
      except Exception:
          sys.exit("Error: can\'t read " + key + " from config.json")
      finally:
          config_data.close()
  return value

if __name__ == '__main__':
    if args.use_https:
        crtPath = readFromConfig('crtPath')
        crtKeyPath = readFromConfig('crtKeyPath')
        app.run(host=args.host, port=args.port, debug=True, ssl_context=(crtPath, crtKeyPath))
    else:
        app.run(host=args.host, port=args.port, debug=True)
