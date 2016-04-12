Flask-Graylog
=============

This is a Flask_ extension that allows you to configure a Graylog_ log handler as well as configuring middleware to log every request/response to Graylog.

.. _Flask: http://flask.pocoo.org/
.. _Graylog: https://graylog.org

Installation
------------

You can install it via `pip`: ::

    pip install Flask-Graylog


Usage
-----

You only need to import and initialize your app ::

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

The following options can be use to configure the graylog logger. ::

    from flask import Flask
    from flask.ext.graylog import Graylog

    app = Flask(__name__)

    # Use configuration from `app`
    app.config['GRAYLOG_HOST'] = '10.1.1.1'
    graylog = Graylog(app)

    # Provide configuration
    config = {'GRAYLOG_HOST': '10.1.1.1'}
    graylog = Graylog(app, config=config)

* `GRAYLOG_HOST` - the host to send messages to [default: 'localhost']
* `GRAYLOG_PORT` - the port to send messages to [default: 12201]
* `GRAYLOG_FACILITY` - the facility to report with [default: 'flask']
* `GRAYLOG_EXTRA_FIELDS` - a dict of extra static fields to include with each message [default: None]
* `GRAYLOG_ADD_DEBUG_FIELDS` - whether extra python debug fields should be added to each message [default: True]
* `GRAYLOG_CONFIGURE_MIDDLEWARE` - whether to setup middleware to log each response [default: True]
