# Salt-event-hub

This is a http server offering an interface to fire salt events in RESTful way.

## Install
* You will need Python 2.6 or higher to get started, so be sure to have an up-to-date Python 2.x installation.
* Install dependencies (`pip install -r requirements.txt`)

## Running
To run **Salt-event-hub** just do:

    % python2 salt-event-hub.py

## command line 
* `--host` - you can set server's listening interface (default is `localhost`)

* `--port` - you can set server's port (default is `5000`)

* `--https` - turn on ssl (default: False)

* `--sslCrt` - path to certificate

* `--sslKey` - path to certificate's key

* `--x_auth_token` - this is the authentication token of the server

* `--pidfile` - set the path for the pid file (default: salt-event-hub.pid)

## config
The Config accepts the same parameters as the command line. In fact both are merged with the command line having priority.

```json
Exemplary config.json:
{
  "x_auth_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ",
  "sslCrt" : "/path/to/config.crt",
  "sslKey" : "/path/to/config.key"
}
```

## REST API
```
POST /<event>/trigger
`The above method expects a payload in json format.`
Example:

% curl -H "X-AUTH-TOKEN: \
eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ" \
-H "Content-Type: application/json" \
-d "{"source":"shell", "project":"projectX"}" \
https://config.example.io:5000/deploy/trigger

=> 200 OK
or
=> 401 Wrong X-AUTH-TOKEN
or
=> 400 Bad Request
```
## Credits
scalable minds - http://scm.io

## License
MIT &copy; scalable minds 2014