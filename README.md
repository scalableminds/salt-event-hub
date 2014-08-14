# Salt-event-hub

This is a http server offering an interface to fire salt events in RESTful way.

## Install
* You will need Python 2.6 or higher to get started, so be sure to have an up-to-date Python 2.x installation.
* Install dependencies (`pip install -r requirements.txt`)

## Testing
You can test your **Salt-event-hub** by running the following.

    % python2 salt-event-hub.py

## Useful commands
* `--host` - you can set server's host (default is `localhost`)

    `% python2 salt-event-hub.py --host example.io`

* `--port` - you can set server's port (default is `5000`)

   `% python2 salt-event-hub.py --port 9000`

* `--https` - in case of using this option you are obligatory to set proper path to certificates and its key (see more in [Config](#config) section)

	`% python2 salt-event-hub.py --https`

## Config
In `config.json` file you can set as well:

* `x_auth_token` - this is an authentication token of server (**WARNING - do not delete this property**)
* `crtPath` - path to certificate
* `crtKeyPath` - path to certificate's key

```
Exemplary config.json:
{
  "x_auth_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ",
  "crtPath" : "/path/to/config.crt",
  "crtKeyPath" : "/path/to/config.key"
}
```
## REST API
```
POST /<event>/trigger
`Above method is expected data in **json format with source and data keys**.`
Example:

% curl -H "X-AUTH-TOKEN: \
eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ" \
"Content-Type: application/json" \
-d "{"source":"oxalis", "data":"xyz"}" \
https://config.example.io:5000/install/trigger

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