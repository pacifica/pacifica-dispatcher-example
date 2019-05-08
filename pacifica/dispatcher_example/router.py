#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher-example: pacifica/dispatcher_example/router.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE and WARRANTY for details.
"""Router for Pacifica Dispatcher Example.

This module defines the router for Pacifica Dispatcher Example.

Attributes:
    router (pacifica.dispatcher.router.Router): The router.

"""

import os

from jsonpath2.path import Path

from pacifica.cli.methods import generate_global_config, generate_requests_auth
from pacifica.dispatcher.downloader_runners import RemoteDownloaderRunner
from pacifica.dispatcher.router import Router
from pacifica.dispatcher.uploader_runners import RemoteUploaderRunner
from pacifica.downloader import Downloader
from pacifica.uploader import Uploader

from .event_handlers import ExampleEventHandler

# Read the configuration for Pacifica CLI.
#
config = generate_global_config()  # type: ConfigParser

# Extract the authentication credentials for HTTP requests from the
# configuration for Pacifica CLI.
#
auth = generate_requests_auth(config)  # type: typing.Dict[str, typing.Any]

# Construct the __remote__ downloader runner using a Pacifica downloader that
# is itself constructed using the configuration for Pacifica CLI and the
# extracted authentication credentials.
#
downloader_runner = RemoteDownloaderRunner(Downloader(cart_api_url=config.get('endpoints', 'download_url'), auth=auth))  # type: pacifica.dispatcher.downloader_runners.RemoteDownloaderRunner

# Construct the __remote__ uploader runner using a Pacifica uploader that is
# itself constructed using the configuration for Pacifica CLI and the extracted
# authentication credentials.
#
uploader_runner = RemoteUploaderRunner(Uploader(upload_url=config.get('endpoints', 'upload_url'), status_url=config.get('endpoints', 'upload_status_url'), auth=auth))  # type: pacifica.dispatcher.uploader_runners.RemoteUploaderRunner

# Construct an __empty__ router.
#
router = Router()  # type: pacifica.dispatcher.router.Router

# Add a new route to the router, so that it is non-empty.
#
# The call to add a new route to the router receives the following arguments:
# 1. The JSONPath, i.e., the instance of the ``jsonpath2.path.Path`` class.
# 2. The event handler, i.e., the instance of the
#    ``pacifica.dispatcher.event_handlers.EventHandler`` class.
#
# In this example, the JSONPath for the example event handler is parsed from the
# content of a text file.
#
router.add_route(Path.parse_file(os.path.join(os.path.dirname(__file__), 'jsonpath2', 'example.txt')), ExampleEventHandler(downloader_runner, uploader_runner))


# Module exports.
#
__all__ = ('router', )
