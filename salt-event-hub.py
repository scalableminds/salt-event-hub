#!/usr/bin/env python2

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

def trigger_event(payload, tag):
    logger.info("Firing event " + tag)
    
    from salt.utils.event import SaltEvent
    sock_dir = '/var/run/salt/master'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, tag)


@app.route('/webhook/github/<authToken>', methods=['POST'])
def github(authToken):

    if auth_token != opts['x_auth_token']:
        abort(401)

    event = request.headers.get("X-GitHub-Event", False)
    if not event:
        abort(400)
    payload = {"data": request.get_json()}
    event_tag = '/'.join(['github', payload['repository']['full_name'], event])

    tigger_event(payload, event_tag)

    return "OK"

@app.route('/<event_tag>/trigger', methods=['POST'])
def trigger(event_tag):
    from salt.utils.event import SaltEvent

    auth_token = request.headers.get("X-AUTH-TOKEN", "")
    if auth_token != opts['x_auth_token']:
      abort(401)

    payload = request.get_json()

    trigger_event(payload, event_tag)

    return "OK"

@app.errorhandler(401)
def custom_401(error):
    return Response('Wrong authorization header', 401, {'Authenticate':'Basic realm="Proper Token Required"'})

def write_pid():
    pid = str(os.getpid())
    pidfile = opts['pidfile']

    if os.path.isfile(pidfile):
        pidfile_pid = open(pidfile).readline().strip()
        if(pid != pidfile_pid):
            print "%s already exists with another pid, exiting (current: %s vs saved: %s)" % (pidfile, pid, pidfile_pid)
            sys.exit()
    else:
        file(pidfile, 'w').write(pid)

def clean_up(*args):
    remove_pid()
    sys.exit(0)

def remove_pid():
    if os.path.isfile(opts['pidfile']):
        os.unlink(opts['pidfile'])

def ensure_clean_up():
    for sig in (SIGINT, SIGTERM, SIGHUP):
        signal(sig, clean_up)
    atexit.register(remove_pid)

def parseCmdLine():
    parser = argparse.ArgumentParser(
        description='Salt-event-hub is a RESTful http server for passing events to saltstack',
        argument_default=argparse.SUPPRESS)

    parser.add_argument('--https', action='store_true', default=False,
                    dest='https',
                    help='Set args if you want send data through https')
    parser.add_argument('--host', default="localhost")
    parser.add_argument('--port', default=5000)
    parser.add_argument("--config", default="config.json")
    parser.add_argument('--pidfile', default="salt-event-hub.pid")
    parser.add_argument('--sslCrt')
    parser.add_argument('--sslKey')
    return parser.parse_args()

def readConfig(config_file):
    try:
        config_data = open(config_file)
    except IOError:
        sys.exit("Error: can\'t find %s" % config_file)
    else:
        data=json.load(config_data)
        config_data.close()
        return data

if __name__ == '__main__':
    args = parseCmdLine()
    cfg = readConfig(args.config)
    global opts
    opts = dict(cfg, **vars(args))

    write_pid()
    ensure_clean_up()
    if opts['https']:
        if("sslCrt" in opts and "sslKey" in opts):
            print opts['sslCrt']
            print opts['sslKey']
            app.run(host=opts['host'], port=opts['port'], ssl_context=(opts['sslCrt'], opts['sslKey']))
        else:
            logger.error("sslCrt and sslKey have to be defined in order to serve https")
            sys.exit(1)
    else:
        app.run(host=opts['host'], port=opts['port'])
