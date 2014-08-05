import logging
import argparse

from logging.handlers import RotatingFileHandler
from flask import Flask
from flask import current_app
from flask import json
from flask import request

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('http')
parser.add_argument('https')

@app.route('/run', methods=['POST'])
def event_listener():
    from salt.utils.event import SaltEvent

    content = request.get_json()
    data = content['data']
    tag = content['tag']
    room = content['room']

    payload = { 'data' : data, 'room' : room }

    sock_dir = '/var/run/salt/minion'
    event = SaltEvent('master', sock_dir)
    event.fire_event(payload, tag)

    return "success"

def debug():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', debug=True, ssl_context=('/Users/new/Documents/Dev/Scalable Minds/certificates/config.crt', '/Users/new/Documents/Dev/Scalable Minds/certificates/config.key'))