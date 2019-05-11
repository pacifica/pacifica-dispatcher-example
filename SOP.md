# Standard Operating Procedure: Modifying Pacifica Dispatcher Example

## Purpose:

To establish guidelines for developing new [Pacifica Dispatcher](https://github.com/pacifica/pacifica-dispatcher) implementations by modifying the [Pacifica Dispatcher Example](https://github.com/pacifica/pacifica-dispatcher-example) implementation.

## Definitions:

**CloudEvents Notification:**
A description of an event according to the [CloudEvents](https://cloudevents.io) specification that is encoded as a JSON object.

**JavaScript Object Notation (JSON):**
A lightweight [data-interchange format](http://json.org/).

**JSONPath:**
An identifier for one-or-more elements of a JSON data structure according to the syntax and semantics of the [`jsonpath2`](https://github.com/pacifica/python-jsonpath2) package.

## Procedure (Summary):

1. Choose new project name.
2. Fork contents of [Git](https://git-scm.com/) repository for [Pacifica Dispatcher Example](https://github.com/pacifica/pacifica-dispatcher-example) implementation.
3. Rename files and directories according to naming convention.
4. Substitute names in file content according to naming convention.
5. Populate `tests/test_files` subdirectory.
6. Develop JSONPaths.
7. Develop event handlers.
8. Configure router.
9. Develop unit tests.

## Procedure:

1. Choose new project name.

2. Fork contents of [Git](https://git-scm.com/) repository for [Pacifica Dispatcher Example](https://github.com/pacifica/pacifica-dispatcher-example) implementation.

3. Rename files and directories according to naming convention.

According to a naming convention, the project name is used in order to generate other names, including: the repository name, the subdirectory name, and the event handler class name.

| Project Name | Repository Name | Subdirectory Name | Event Handler Class Name | Unit Test Class Name |
|:-:|:-:|:-:|:-:|:-:|
| {name} | pacifica-dispatcher-{name} | `pacifica/dispatcher_{name}` | `{name}EventHandler` | `{name}TestCase` |
| Example | pacifica-dispatcher-example | `pacifica/dispatcher_example` | `ExampleEventHandler` | `ExampleTestCase` |
| Hello, world! | pacifica-dispatcher-hello-world | `pacifica/dispatcher_hello_world` | `HelloWorldEventHandler` | `HelloWorldTestCase` |

The repository name is "pacifica-dispatcher-{name}", where "{name}" is substituted for the project name.
All non-alphanumeric characters in the project name are removed.
Spans of one-or-more whitespace characters are replaced with a hyphen "-" character.

The subdirectory name is `pacifica/dispatcher_{name}`, where "{name}" is substituted for the project name.
All non-alphanumeric characters in the project name are removed.
Spans of one-or-more whitespace characters are replaced with an underscore "\_" character.

The event handler and unit test class names are `{name}EventHandler` and `{name}TestCase`, respectively, where "{name}" is substituted for the project name.
All non-alphanumeric characters in the project name are removed.
Spans of one-or-more alphanumeric characters are written in UpperCamelCase.
Spans of one-or-more whitespace characters are removed.

The following files are affected:
 * `pacifica/dispatcher_example` &rarr; `pacifica/dispatcher_{name}`
 * `pacifica/dispatcher_example/jsonpath2/example.txt` &rarr; `pacifica/dispatcher_{name}/jsonpath2/{name}.txt`
 * `tests/example_test.py` &rarr; `tests/{name}_test.py`

4. Substitute names in file content according to naming convention.

The following files are affected:
 * `.github/ISSUE_TEMPLATE.md`
 * `.travis.yml`
 * `Dockerfile.celery`
 * `Dockerfile.uwsgi`
 * `README.md`
 * `appveyor.yml`
 * `docker-compose.yml`
 * `pacifica/__init__.py`
 * `pacifica/dispatcher_{name}/__init__.py`
 * `pacifica/dispatcher_{name}/__main__.py`
 * `pacifica/dispatcher_{name}/event_handlers.py`
 * `pacifica/dispatcher_{name}/router.py`
 * `setup.py`
 * `tests/example_test.py`

5. Populate `tests/test_files` subdirectory.

The `tests/test_files` subdirectory has the following structure:

 * `tests/test_files`
   * `eventID1`
     * `data`
       * `file1`
       * &hellip;
       * `fileN`
     * `event.json`
   * &hellip;
   * `eventIDN`
     * `data`
       * `file1`
       * &hellip;
       * `fileN`
     * `event.json`

The structure is a set of subdirectories, where each subdirectory contains:
 * `event.json` - The [CloudEvents](https://cloudevents.io) notification for the test case; and
 * `data` - The files for the test case (as described in the [CloudEvents](https://cloudevents.io) notification).

A [CloudEvents](https://cloudevents.io) notification that is emitted by [Pacifica Metadata](https://github.com/pacifica/pacifica-metadata) is a [JSON](http://json.org/) object with the following structure:

```json
{
  "cloudEventsVersion": "0.1",
  "contentType": "application/json",
  "data": [
    {
      "destinationTable": "Transactions._id",
      "value": -1
    },
    {
      "destinationTable": "Transactions.submitter",
      "value": -1
    },
    {
      "destinationTable": "Transactions.project",
      "value": -1
    },
    {
      "destinationTable": "Transactions.instrument",
      "value": -1
    },
    {
      "destinationTable": "TransactionKeyValue",
      "key": "example-key",
      "value": "example-value"
    },
    {
      "_id": 1,
      "ctime": "Thu Aug 30 15:19:40 PST 2018",
      "destinationTable": "Files",
      "hashsum": "4b5e3e59af149a058366bed86b05500c0acd34e0",
      "hashtype": "sha1",
      "mimetype": "text/plain",
      "mtime": "Thu Aug 30 15:19:40 PST 2018",
      "name": "lipsum.txt",
      "size": 614,
      "subdir": ""
    }
  ],
  "eventID": "C234-1234-1234",
  "eventTime": "2018-08-30T15:20:00Z",
  "eventType": "org.pacifica.metadata.ingest",
  "source": "/pacifica/metadata/ingest"
}
```

| Attribute Name | Description |
| :-: | :- |
| `"cloudEventsVersion"` | The version of the [CloudEvents](https://cloudevents.io) specification. The value of this attribute is always `"0.1"`. |
| `"contentType"` | The MIME type for the [CloudEvents](https://cloudevents.io) notification. The value of this attribute is always `"application/json"`. |
| `"data"` | The payload for the [CloudEvents](https://cloudevents.io) notification. The value of this attribute is arbitrary and specific to the values of the `"eventType"` and `"source"` attributes. |
| `"eventID"` | The unique identifier for the [CloudEvents](https://cloudevents.io) notification. The value of this attribute is arbitrary. |
| `"eventTime"` | The timestamp for the [CloudEvents](https://cloudevents.io) notification. The value of this attribute is a string in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) date and time format. |
| `"eventType"` | The unique identifier for the type of the [CloudEvents](https://cloudevents.io) notification. For [Pacifica Metadata](https://github.com/pacifica/pacifica-metadata), the value of this attribute is always `"org.pacifica.metadata.ingest"`. |
| `"source"` | The unique identifier for the source of the [CloudEvents](https://cloudevents.io) notification. For [Pacifica Metadata](https://github.com/pacifica/pacifica-metadata), the value of this attribute is always `"/pacifica/metadata/ingest"`. |

The name of the subdirectory corresponds to the value of the `"eventID"` attribute for the CloudEvents notification, e.g., `tests/test_files/C234-1234-1234` &rarr; `"C234-1234-1234"`.

The value of the `"data"` attribute is a [JSON](http://json.org/) array:
```json
"data": [
  ...
],
```

 The elements of the [JSON](http://json.org/) array constitute a description of the metadata for:
 * 1 transaction;
 * 0..N transaction key-value pairs; and
 * 0..N files.

The unique identifier for the transaction, along with the unique identifiers for the submitter, project and instrument are described as follows:
```json
"data": [
  {
    "destinationTable": "Transactions._id",
    "value": -1
  },
  {
    "destinationTable": "Transactions.submitter",
    "value": -1
  },
  {
    "destinationTable": "Transactions.project",
    "value": -1
  },
  {
    "destinationTable": "Transactions.instrument",
    "value": -1
  },
  ...
],
```

Transaction key-value pairs are described as follows:
```json
"data": [
  ...
  {
    "destinationTable": "TransactionKeyValue",
    "key": "example-key",
    "value": "example-value"
  },
  ...
],
```

Each transaction key-value pair has `"key"` and `"value"` attribute-value pairs.
In the above example, the key is `"example-key"` and the value is `"example-value"`.

Files are described as follows:
```json
"data": [
  ...
  {
    "_id": 1,
    "ctime": "Thu Aug 30 15:19:40 PST 2018",
    "destinationTable": "Files",
    "hashsum": "4b5e3e59af149a058366bed86b05500c0acd34e0",
    "hashtype": "sha1",
    "mimetype": "text/plain",
    "mtime": "Thu Aug 30 15:19:40 PST 2018",
    "name": "lipsum.txt",
    "size": 614,
    "subdir": ""
  }
],
```

In the above example, the value of the `"hashsum"` attribute is computed with respect to the value of the `"hashtype"` attribute using the following command:
```bash
bash$ openssl sha1 tests/test_files/C234-1234-1234/data/lipsum.txt
SHA1(tests/test_files/C234-1234-1234/data/lipsum.txt)= 4b5e3e59af149a058366bed86b05500c0acd34e0
```

The value of the `"mimetype"` attribute is computed using the following command:
```bash
bash$ file --mime tests/test_files/C234-1234-1234/data/lipsum.txt
tests/test_files/C234-1234-1234/data/lipsum.txt: text/plain; charset=us-ascii
```

The value of the `"size"` attribute is computed using the following command:
```bash
bash$ wc -c tests/test_files/C234-1234-1234/data/lipsum.txt
     614 tests/test_files/C234-1234-1234/data/lipsum.txt
```

6. Develop JSONPaths.

The recommended storage location for JSONPaths is the `pacifica/dispatcher_{name}/jsonpath2` subdirectory.

Each JSONPath must match the root element of the [CloudEvents](https://cloudevents.io) notification **exactly once**.

The minimum JSONPath for a [CloudEvents](https://cloudevents.io) notification is:
```
$[?(
  $["eventID"]
)]
```

In English, the above JSONPath reads:
_"Match the root element of the JSON object if it has an `"eventID"` attribute."_

The minimum JSONPath for a [CloudEvents](https://cloudevents.io) notification that is emitted by [Pacifica Metadata](https://github.com/pacifica/pacifica-metadata) is:
```
$[?(
  $["eventID"]
    and
  $["eventType"] = "org.pacifica.metadata.ingest"
    and
  $["source"] = "/pacifica/metadata/ingest"
)]
```

In English, the above JSONPath reads: _"Match the root element of the JSON object if (a) it has an `"eventID"` attribute, (b) it has an `"eventType"` attribute whose value is `"org.pacifica.metadata.ingest"`, and (c) it has a `"source"` attribute whose value is `"/pacifica/metadata/ingest"`."_

The JSONPath for the example is:
```
$[?(
  $["data"][*][?(
    @["destinationTable"] = "TransactionKeyValue"
      and
    @["key"] = "example-key"
      and
    @["value"] = "example-value"
  )]
    and
  $["data"][*][?(
    @["destinationTable"] = "Files"
      and
    @["mimetype"] = "text/plain"
      and
    @["subdir"] = ""
  )]
    and
  $["eventID"]
    and
  $["eventType"] = "org.pacifica.metadata.ingest"
    and
  $["source"] = "/pacifica/metadata/ingest"
)]
```

In English, the above JSONPath reads: _"Match the root element of the JSON object if (a) it has an `"eventID"` attribute, (b) it has an `"eventType"` attribute whose value is `"org.pacifica.metadata.ingest"`, (c) it has a `"source"` attribute whose value is `"/pacifica/metadata/ingest"`, (d) it has a transaction key-value pair where the key is `"example-key"` and the value is `"example-value"`, and (e) it has a file in the root `""` subdirectory whose MIME type is `"text/plain"`."_

> **Tip:** For more information about JSONPath syntax and semantics, please consult the documentation for the  [`jsonpath2`](https://github.com/pacifica/python-jsonpath2) package.

7. Develop event handlers.

The recommended location for event handlers is the `pacifica/dispatcher_{name}/event_handlers.py` source file.

An event handler is a subclass of the [`pacifica.dispatcher.event_handlers.EventHandler`](https://github.com/pacifica/pacifica-dispatcher/blob/master/pacifica/dispatcher/event_handlers.py) class.

```python
from cloudevents.model import Event
from pacifica.dispatcher.event_handlers import EventHandler

class YourEventHandler(EventHandler):
  def handle(self, event: Event) -> None:
    # YOUR CODE GOES HERE
    pass
```

The implementation of the `handle` method may use any Python package that is installed on the system.
List third-party software packages in `requirements.txt` (see https://pip.pypa.io/en/stable/user_guide/#requirements-files for more information).

> **Tip:** An example implementation of an event handler that downloads files, does work and then uploads the result is given in the `pacifica/pacifica_{name}/event_handlers.py` source file.

8. Configure router.

The recommended location for the router is the `pacifica/dispatcher_{name}/router.py` source file.

The empty router is constructed as follows:
```python
from pacifica.dispatcher.router import Router

router = Router()

# YOUR ROUTES GO HERE
```

New routes are added to the router using the [`add_route`](https://github.com/pacifica/pacifica-dispatcher/blob/master/pacifica/dispatcher/router.py#L62) method.
Each route consists of a JSONPath and an event handler.
If the JSONPath matches successfully, then the `handle` method of the event handler is called.

```python
import os

from jsonpath2.path import Path
from pacifica.dispatcher.router import Router

from .event_handlers import YourEventHandler

router = Router()

router.add_route(Path.parse_file(os.path.join(os.path.dirname(__file__), 'jsonpath2', 'example.txt')), YourEventHandler())
```
In the above example, the `pacifica/dispatcher_{name}/jsonpath2/example.txt` file contains the JSONPath.
The [`os.path.join`](https://docs.python.org/3/library/os.path.html#os.path.join) method is used to construct the path to the JSONPath file in order to maintain platform independence.

9. Develop unit tests.

The recommended location for unit tests is the `tests/{name}_test.py` source file.

Unit tests should be developed for the following aspects of the implementation:
 * That the `handle` method of each event handler may be called without raising an uncaught exception;
 * That each JSONPath matches the corresponding [CloudEvents](https://cloudevents.io) notification; and
 * That each route matches the corresponding [CloudEvents](https://cloudevents.io) notification.

Units tests are run with the following commands:
```bash
bash$ cd tests
bash$ python3 -m unittest {name}_test.py
```
where `{name}` is substituted for the project name according to the naming convention.

> **Tip:** An example implementation of the unit tests is given in the `tests/{name}_test.py` source file.
