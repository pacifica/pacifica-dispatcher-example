# Configuration

The Pacifica Core services require two configuration files. The REST
API utilizes [CherryPy](https://github.com/cherrypy) and review of
their
[configuration documentation](http://docs.cherrypy.org/en/latest/config.html)
is recommended. The service configuration file is a INI formatted
file containing configuration for database connections.

## CherryPy Configuration File

An example of UniqueID server CherryPy configuration:

```ini
[global]
log.screen: True
log.access_file: 'access.log'
log.error_file: 'error.log'
server.socket_host: '0.0.0.0'
server.socket_port: 8051

[/]
request.dispatch: cherrypy.dispatch.MethodDispatcher()
tools.response_headers.on: True
tools.response_headers.headers: [('Content-Type', 'application/json')]
```

## Starting the Service

Starting the UniqueID service can be done by two methods. However,
understanding the requirements and how they apply to REST services
is important to address as well. Using the
internal CherryPy server to start the service is recommended for
Windows platforms. For Linux/Mac platforms it is recommended to
deploy the service with
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

### Deployment Considerations

### CherryPy Server

To make running the UniqueID service using the CherryPy's builtin
server easier we have a command line entry point.

```
$ pacifica-uniqueid --help
usage: pacifica-uniqueid [-h] [-c CONFIG] [-p PORT] [-a ADDRESS]

Run the uniqueid server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        cherrypy config file
  -p PORT, --port PORT  port to listen on
  -a ADDRESS, --address ADDRESS
                        address to listen on
$ pacifica-uniqueid-cmd dbsync
$ pacifica-uniqueid
[09/Jan/2019:09:17:26] ENGINE Listening for SIGTERM.
[09/Jan/2019:09:17:26] ENGINE Bus STARTING
[09/Jan/2019:09:17:26] ENGINE Set handler for console events.
[09/Jan/2019:09:17:26] ENGINE Started monitor thread 'Autoreloader'.
[09/Jan/2019:09:17:26] ENGINE Serving on http://0.0.0.0:8051
[09/Jan/2019:09:17:26] ENGINE Bus STARTED
```

### uWSGI Server

To make running the UniqueID service using uWSGI easier we have a
module to be included as part of the uWSGI configuration. uWSGI is
very configurable and can use this module many different ways. Please
consult the
[uWSGI Configuration](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html)
documentation for more complicated deployments.

```
$ pip install uwsgi
$ uwsgi --http-socket :8051 --master -p 1 --module pacifica.uniqueid.wsgi
```
