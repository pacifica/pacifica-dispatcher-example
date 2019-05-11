# Pacifica Dispatcher Example

This package provides an example implementation of a [Pacifica Dispatcher](https://github.com/pacifica/pacifica-dispatcher).

## Overview

This package is divided into the following source files:

 * `pacifica/`
   * `__init__.py` = The namespace declaration for the parent `pacifica` package.
   * `dispatcher_example/`
     * `__init__.py` = The initializer for this package.
     * `__main__.py` = The entrypoint for this package.
     * `event_handlers.py` = The event handlers for this package.
     * `router.py` = The router for this package.

Please read the source files for more information about their content.

## Installation Guide

This package is installed using the following commands:

 1. `python3 -m pip install -e .`

## Testing Guide

This package is tested using the following commands:

 1. `cd tests`
 2. `python3 -m unittest example_test.py`

## Start-up Guide

This package is started in three stages, where each stage occurs in a separate
terminal emulator session:
 1. The message queue is started;
 2. The worker for the task queue is started; and
 3. The web server is started.

The message queue is started using the following commands:
 1. `docker-compose up rabbit`

The worker for the task queue is started using the following commands:
 1. `env DATABASE_URL="sqliteext:///db.sqlite3" celery -A "pacifica.dispatcher_example.__main__:celery_app" worker -l info`

The web server is started using the following commands:
 1. `env DATABASE_URL="sqliteext:///db.sqlite3" python3 -m "pacifica.dispatcher_example.__main__"`

**Note:** The `DATABASE_URL` environment variable specifies the connection URL
for the database. In this guide, the database is managed using
[SQLite](https://sqlite.org), where the database itself is stored in the
`db.sqlite3` file in the root directory of this package.
