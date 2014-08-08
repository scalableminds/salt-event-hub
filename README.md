# Salt-event-hub

This is a http server offering an interface to fire salt events in RESTful way.

## Install
* You will need Python 2.6 or higher to get started, so be sure to have an up-to-date Python 2.x installation.
* Install Flask (`pip install Flask`)

## Testing
You can test your **Salt-event-hub** by running the following.

    % python2 salt-event-hub.py

## Useful commands
* `--host` - you can set server's host (default is `localhost`
    
    `% python2 salt-event-hub.py --host scm.io`
    
* `--port` - you can set server's port (default is `5000`)
    `% python2 salt-event-hub.py --host 9000`
    
* `--https` - in case of using this option you are obligatory to set proper path to certificates and its key (see more in [Config]() section)
	`% python2 salt-event-hub.py --https`
	
## Config
In `config.json` file you can change (**WARNING - do not delete these properties**):

* `crt` - path to certificate
* `crtKey` - path to certificate's key
* `x_auth_token` - this is an authentication token of server

## REST API
```
POST /<action>/trigger
Example:

% curl -H "X-AUTH-TOKEN: \ 
eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ" \
"Content-Type: application/json" \ 
-d "{"source":"oxalis", "data":"xyz"}" \
-https://config.example.io:5000/install/trigger

=> 200 OK
or
=> 401 Wrong X-AUTH-TOKEN
or
=> 400 Bad Request
```
## Credits
scalable minds - http://scm.io

## License
TBD