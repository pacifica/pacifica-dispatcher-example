#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher-example: tests/example_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE and WARRANTY for details.
"""Test cases for Pacifica Dispatcher Example.

This module defines the test cases for Pacifica Dispatcher Example.

"""

import json
import os
import unittest

from cloudevents.model import Event
from jsonpath2.path import Path

from pacifica.dispatcher.downloader_runners import LocalDownloaderRunner
from pacifica.dispatcher.uploader_runners import LocalUploaderRunner

from pacifica.dispatcher_example.event_handlers import ExampleEventHandler
from pacifica.dispatcher_example.router import router


class ExampleTestCase(unittest.TestCase):
    """Test cases for Pacifica Dispatcher Example.

    Attributes:
        basedir_name (str): The name of the base directory for the CloudEvents
            notification that will be used when running the test cases.
        event_data (typing.Dict[str, typing.Any]): The JSON-encoded data for the
            CloudEvents notification.

    """

    def setUp(self) -> None:
        """Initialize the environment for the test cases.

        """

        # Set the name of the base directory for the CloudEvents notification
        # that will be used when running the test cases.
        #
        self.basedir_name = os.path.abspath(os.path.join('test_files', 'C234-1234-1234'))  # type: str

        # Read the JSON-encoded data for the CloudEvents notification.
        #
        with open(os.path.join(self.basedir_name, 'event.json'), mode='r') as event_file:
            self.event_data = json.load(event_file)  # type: typing.Dict[str, typing.Any]

    def test_example_event_handler(self) -> None:
        """Test the event handler for Pacifica Downloader Example.

        """

        # Construct the CloudEvents notification object using the JSON-encoded
        # data.
        #
        event = Event(self.event_data)  # type: cloudevents.model.Event

        # Construct the __local__ downloader runner using the name of the base
        # directory. The files to be downloaded are located in the "data"
        # subdirectory.
        #
        downloader_runner = LocalDownloaderRunner(os.path.join(self.basedir_name, 'data'))

        # Construct the __local__ uploader runner.
        #
        uploader_runner = LocalUploaderRunner()

        # Construct the event handler using the downloader and uploader runners.
        #
        event_handler = ExampleEventHandler(downloader_runner, uploader_runner)

        # Verify that the event handler successfully handles the CloudEvents
        # notification without raising an exception.
        #
        self.assertEqual(None, event_handler.handle(event))

    def test_example_jsonpath2_path(self) -> None:
        """Test the JSONPath for Pacifica Dispatcher Example.

        """

        # Construct the JSONPath for the example event handler by parsing the
        # content of a text file.
        #
        path = Path.parse_file(os.path.join(os.path.dirname(__file__), '..', 'pacifica', 'dispatcher_example', 'jsonpath2', 'example.txt'))  # type: jsonpath2.path.Path

        # Verify that the JSONPath successfully matches the JSON-encoded data
        # for the CloudEvents notification.
        #
        self.assertEqual(1, len(list(path.match(self.event_data))))

    def test_example_router(self) -> None:
        """Test the router for Pacifica Dispatcher Example.

        """

        # Verify that the router successfully matches the JSON-encoded data for
        # the CloudEvents notification.
        #
        self.assertEqual(1, len(list(router.match(self.event_data))))


# Entrypoint.
#
if __name__ == '__main__':
    unittest.main()
