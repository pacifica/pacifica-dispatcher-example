#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher-example: pacifica/dispatcher_example/event_handlers.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE and WARRANTY for details.
"""Event handlers for Pacifica Dispatcher Example.

This module defines the event handler for Pacifica Dispatcher Example.

Attributes:
    ExampleEventHandler (type): The class for the event handler.

"""

import os
import tempfile

from cloudevents.model import Event

from pacifica.dispatcher.downloader_runners import DownloaderRunner
from pacifica.dispatcher.event_handlers import EventHandler
from pacifica.dispatcher.models import File, Transaction, TransactionKeyValue
from pacifica.dispatcher.uploader_runners import UploaderRunner


class ExampleEventHandler(EventHandler):
    """An example implementation of an event handler that reads each file and
    then writes a copy of the file with all the cased characters converted to
    uppercase.

    Attributes:
        downloader_runner (pacifica.dispatcher.downloader_runners.DownloaderRunner): The downloader runner to use.
        uploader_runner (pacifica.dispatcher.uploader_runners.UploaderRunner): The uploader runner to use.

    """

    def __init__(self, downloader_runner: DownloaderRunner, uploader_runner: UploaderRunner) -> None:
        """Initialize this event handler.

        Args:
            downloader_runner (pacifica.dispatcher.downloader_runners.DownloaderRunner): The downloader runner to use.
            uploader_runner (pacifica.dispatcher.uploader_runners.UploaderRunner): The uploader runner to use.

        """

        super(ExampleEventHandler, self).__init__()
        self.downloader_runner = downloader_runner
        self.uploader_runner = uploader_runner

    def handle(self, event: Event) -> None:
        """Handle a CloudEvents notification.

        Args:
            event (cloudevents.model.Event): The CloudEvents notification to
                handle.

        """

        # Extract the metadata descriptions for the Pacifica transaction,
        # transaction key-values and files from the payload of the CloudEvents
        # notification.
        #
        transaction_inst = Transaction.from_cloudevents_model(event)  # type: pacifica.dispatcher.models.Transaction
        transaction_key_value_insts = TransactionKeyValue.from_cloudevents_model(event)  # type: typing.List[pacifica.dispatcher.models.TransactionKeyValue]
        file_insts = File.from_cloudevents_model(event)  # type: typing.List[pacifica.dispatcher.models.File]

        # Create a temporary directory for the files that will be downloaded by
        # the downloader runner.
        #
        with tempfile.TemporaryDirectory() as downloader_tempdir_name:
            # Create a temporary directory for the files that will be uploaded
            # by the uploader runner.
            #
            with tempfile.TemporaryDirectory() as uploader_tempdir_name:
                # Download the files to the temporary directory using the
                # downloader runner.
                #
                # The return value for this function call is a list of callables,
                # where each callable delegates to the ``open`` built-in
                # function and returns an IO object.
                #
                # The ordering of the return value is the same as that of the
                # list of metadata descriptions for Pacifica files.
                #
                file_openers = self.downloader_runner.download(downloader_tempdir_name, file_insts)  # type: typing.List[typing.Callable[[], typing.TextIO]]

                # Use the ``zip`` built-in function to associate the metadata
                # descriptions for Pacifica files with the callables.
                #
                for file_inst, file_opener in zip(file_insts, file_openers):
                    # Open the original file.
                    #
                    with file_opener() as file:
                        # Open a new file in write-only mode that is to be
                        # uploaded by the uploader runner.
                        #
                        # In this example, the relative path to the new file is
                        # the same relative path to the original file.
                        #
                        with open(os.path.join(uploader_tempdir_name, file_inst.path), mode='w') as new_file:
                            # Read the content of the original file and then
                            # write a copy of the content with all the cased
                            # characters converted to uppercase.
                            new_file.write(file.read().upper())

                # Construct the metadata description for the new Pacifica
                # transaction.
                #
                # In this example, the "submitter", "instrument" and "project"
                # attributes from the original metadata description are reused.
                #
                new_transaction_inst = Transaction(submitter=transaction_inst.submitter, instrument=transaction_inst.instrument, project=transaction_inst.project)  # type: pacifica.dispatcher.models.Transaction

                # Construct the metadata descriptions for the new Pacifica
                # key-values.
                #
                new_transaction_key_value_insts = [
                    # In this example, the relationship between the original and new
                    # Pacifica transactions is asserted via the "Transactions._id"
                    # key and its value, the ID for the original Pacifica
                    # transaction.
                    #
                    # This is an example of the assertion of retrospective
                    # provenance information.
                    #
                    TransactionKeyValue(key='Transactions._id', value=transaction_inst._id),
                    # In this example, a second Pacifica transaction key-value
                    # is asserted via the "example-key" and its value.
                    #
                    TransactionKeyValue(key='example-key', value='example-value'),
                ]  # type: typing.List[pacifica.dispatcher.models.TransactionKeyValue]

                # Upload the files in the temporary directory using the uploader
                # runner.
                #
                # The return value for this function call is a tuple of the
                # uploader's bundle, the job ID for the upload, and the state of
                # the upload.
                #
                (_bundle, _job_id, _state) = self.uploader_runner.upload(uploader_tempdir_name, transaction=new_transaction_inst, transaction_key_values=new_transaction_key_value_insts)  # type: typing.Tuple[pacifica.uploader.bundler.Bundler, int, typing.Dict[str, typing.Any]]


# Module exports.
#
__all__ = ('ExampleEventHandler', )
