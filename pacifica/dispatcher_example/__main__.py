#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher-example: pacifica/dispatcher_example/__main__.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE and WARRANTY for details.
"""Entrypoint for Pacifica Dispatcher Example.

This module provides the entrypoint for Pacifica Dispatcher Example as a script
that connects to the database via `Peewee`_, starts and/or connects to a task
queue using `Celery`_, and then starts a `CherryPy`_ server and listens for
connections.

Attributes:
    ReceiveTaskModel (type): The class for the `Peewee`_ model that encapsulates
        the concept of receiving and handling a `CloudEvents`_ notification.
    application (cherrypy.Application): The `CherryPy`_ application.
    celery_app (celery.Celery): The `Celery`_ application.
    db (peewee.Database): The `Peewee`_ database.
    main (typing.Callable[[], None]): The entrypoint function.

.. _Celery:
   http://www.celeryproject.org/
.. _CherryPy:
   https://cherrypy.org/
.. _CloudEvents:
   https://cloudevents.io/
.. _Peewee:
   http://peewee-orm.com/

"""

import argparse
import os

import cherrypy
import playhouse.db_url

from pacifica.dispatcher.receiver import create_peewee_model

from .router import router


# Connect to the database using the URL connection string.
#
# The URL connection string is read from the "DATABASE_URL" environment
# variable. If the "DATABASE_URL" environment variable is undefined, then the
# default behavior is to connect to an in-memory SQLite database.
#
db = playhouse.db_url.connect(os.getenv('DATABASE_URL', 'sqlite:///:memory:'))  # type: peewee.Database

# Construct the Peewee model.
#
ReceiveTaskModel = create_peewee_model(db)  # type: type

# Create the database table for the Peewee model.
#
# The "safe" keyword argument ensures that the database table is only created if
# it does not exist.
#
ReceiveTaskModel.create_table(safe=True)

# Construct the Celery application for the Peewee model.
#
# The arguments for the constructor are as follows:
# 1. The Pacifica Dispatcher router.
# 2. The name of the Celery application's task queue.
# 3. The name of the Celery task that is triggered when a CloudEvents
#    notification is received.
#
# The URL connection string for the Celery application's backend is read from
# the "BACKEND_URL" environment variable.
#
# The URL connection string for the Celery application's message broker is read
# from the "BROKER_URL" environment variable.
#
celery_app = ReceiveTaskModel.create_celery_app(router, 'pacifica.dispatcher_example.app', 'pacifica.dispatcher_example.tasks.receive', backend=os.getenv('BACKEND_URL', 'rpc://'), broker=os.getenv('BROKER_URL', 'pyamqp://'))

# Construct the CherryPy application for the Peewee model.
#
# The arguments for the constructor are as follows:
# 1. The Celery task that is triggered when a CloudEvents notification is
#    received.
#
application = ReceiveTaskModel.create_cherrypy_app(celery_app.tasks['pacifica.dispatcher_example.tasks.receive'])


def main() -> None:
    """Entrypoint function.

    Note:
        This function has no arguments or keyword arguments and does not return
        a value.

    """

    # Construct the parser for command-line arguments.
    #
    parser = argparse.ArgumentParser(description='Start the CherryPy application and listen for connections.')
    parser.add_argument('--config', metavar='CONFIG', dest='config', type=str, default=None, help='The CherryPy configuration file (overrides host and port options).')
    parser.add_argument('--host', metavar='HOST', dest='host', type=str, default='127.0.0.1', help='The hostname or IP address on which to listen for connections.')
    parser.add_argument('--port', metavar='PORT', dest='port', type=int, default=8069, help='The TCP port on which to listen for connections.')

    # Parse the command-line arguments.
    #
    args = parser.parse_args()

    # Configure CherryPy using the command-line arguments.
    #
    cherrypy.config.update({
        'global': {
            'server.socket_host': args.host,
            'server.socket_port': args.port,
        },
    })

    if args.config is not None:
        # Configure CherryPy using the command-line-argument-specified configuration file.
        #
        cherrypy.config.update(args.config)

    # Mount the CherryPy application.
    #
    cherrypy.tree.mount(application)

    # Start the CherryPy application and listen for connections.
    #
    cherrypy.engine.start()
    cherrypy.engine.block()


# Module exports.
#
__all__ = ('ReceiveTaskModel', 'application', 'celery_app', 'db', 'main', )


# Entrypoint.
#
if __name__ == '__main__':
    main()
