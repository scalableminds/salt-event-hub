import logging
import argparse
import sys
import os
import atexit
from signal import *

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
parser.add_argument('--https', action='store_true', default=False,
                    dest='use_https',
                    help='Set args if you want send data through https')
parser.add_argument('--host', default="localhost")
parser.add_argument('--port', default=5000)
parser.add_argument('--pidfile', default="salt-event-hub.pid")
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

    sock_dir = '/var/run/salt/master'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, action)

    return "OK"

@app.errorhandler(401)
def custom_401(error):
    return Response('Wrong X-AUTH-TOKEN', 401, {'Authenticate':'Basic realm="Proper Token Required"'})

def write_pid():
    pid = str(os.getpid())
    pidfile = args.pidfile

    if os.path.isfile(pidfile):
        print "%s already exists, exiting" % pidfile
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)

def clean_up(*args):
    remove_pid()
    sys.exit(0)

def remove_pid():
    pidfile = args.pidfile
    if os.path.isfile(pidfile):
        os.unlink(pidfile)

def ensure_clean_up():
    for sig in (SIGINT, SIGTERM):
        signal(sig, clean_up)
    atexit.register(remove_pid)

if __name__ == '__main__':
    write_pid()
    ensure_clean_up()
    if args.use_https:
        app.run(host=args.host, port=args.port, ssl_context=(crt, crtKey))
    else:
        app.run(host=args.host, port=args.port)

