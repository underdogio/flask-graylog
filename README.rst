Flask-Graylog
=============

This is a Flask_ extension that allows you to configure a Graylog_ log handler as well as configuring middleware to log every request/response to Graylog.

.. _Flask: http://flask.pocoo.org/
.. _Graylog: https://graylog.org

Installation
------------

You can install it via `pip`:

.. code:: bash

    pip install Flask-Graylog


Usage
-----

You only need to import and initialize your app

.. code:: python

    # Import dependencies
    from flask import Flask
    from flask.ext.graylog import Graylog

    # Configure app and Graylog logger
    app = Flask(__name__)
    graylog = Graylog(app)

    # Log to graylog
    graylog.info('Message', extra={
        'extra': 'metadata',
    })

    # Use graylog log handler in another logger
    import logging
    logger = logging.getLogger(__name__)
    logger.addHandler(graylog.handler)
    logger.info('Message')


Configuration options
~~~~~~~~~~~~~~~~~~~~~

The following options can be use to configure the graylog logger.

.. code:: python

    from flask import Flask
    from flask.ext.graylog import Graylog

    app = Flask(__name__)

    # Use configuration from `app`
    app.config['GRAYLOG_HOST'] = '10.1.1.1'
    graylog = Graylog(app)

    # Provide configuration
    config = {'GRAYLOG_HOST': '10.1.1.1'}
    graylog = Graylog(app, config=config)

* ``GRAYLOG_HOST`` - the host to send messages to [default: 'localhost']
* ``GRAYLOG_PORT`` - the port to send messages to [default: 12201]
* ``GRAYLOG_FACILITY`` - the facility to report with [default: 'flask']
* ``GRAYLOG_EXTRA_FIELDS`` - whether or not to include the `extra` data from each message [default: True]
* ``GRAYLOG_ADD_DEBUG_FIELDS`` - whether extra python debug fields should be added to each message [default: True]
* ``GRAYLOG_CONFIGURE_MIDDLEWARE`` - whether to setup middleware to log each response [default: True]


Example message format
~~~~~~~~~~~~~~~~~~~~~~

.. code:: json

   {
        "_process_name": "MainProcess",
        "_request": {
            "content_length": "",
            "remote_addr": "127.0.0.1",
            "headers": {
                "upgrade_insecure_requests": "1",
                "connection": "keep-alive",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "dnt": "1",
                "host": "localhost:5000",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
                "accept_language": "en-US,en;q=0.8,ms;q=0.6",
                "cache_control": "max-age=0",
                "accept_encoding": "gzip, deflate, sdch"
            },
            "path_info": "/",
            "content_type": "",
            "query_string": "",
            "method": "GET"
        },
        "level": 6,
        "_logger": "flask_graylog",
        "timestamp": 1460502169.950895,
        "_pid": 6010,
        "facility": "flask",
        "_function": "after_request",
        "_thread_name": "Thread-1",
        "host": "voltaire.local",
        "version": "1.0",
        "file": "Flask-Graylog/flask_graylog.py",
        "full_message": "Finishing request for \"GET http://localhost:5000/\" from -",
        "line": 130,
        "_response": {
            "headers": {
                "content_length": "6",
                "content_type": "text/html; charset=utf-8"
            },
            "time_ms": 0,
            "status_code": 200
        },
        "_flask": {
            "view_args": {},
            "endpoint": "root"
        },
        "short_message": "Finishing request for \"GET http://localhost:5000/\" from -"
    }
