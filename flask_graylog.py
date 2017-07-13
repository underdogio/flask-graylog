import logging
import time

from flask import g, request
import graypy


class Graylog(logging.Logger):
    __slots__ = ['app', 'config', 'handler']

    def __init__(self, app=None, config=None, level=logging.NOTSET):
        """
        Constructor for flask.ext.graylog.Graylog

        :param app: Flask application to configure for graylog
        :type app: `flask.Flask` or `None`
        :param config: Configuration to use instead of `app.config`
        :type config: `dict` or `None`
        :param level: The logging level to set for this handler
        :type level: `int`
        """
        super(Graylog, self).__init__(__name__, level=level)

        # Save their config for later
        self.config = config

        # If we have an app, then call `init_app` automatically
        if app is not None:
            self.init_app(app, self.config)

    def init_app(self, app, config=None):
        """
        Configure Graylog logger from a Flask application

        Available configuration options:

          GRAYLOG_HOST - the host to send messages to [default: 'localhost']
          GRAYLOG_PORT - the port to send messages to [default: 12201]
          GRAYLOG_FACILITY - the facility to report with [default: 'flask']
          GRAYLOG_EXTRA_FIELDS - whether or not to include `extra` fields from the message [default: True]
          GRAYLOG_ADD_DEBUG_FIELDS - whether extra python debug fields should be added to each message [default: True]
          GRAYLOG_CONFIGURE_MIDDLEWARE - whether to setup middleware to log each response [default: True]

        :param app: Flask application to configure this logger for
        :type app: flask.Flask
        :param config: An override config to use instead of `app.config`
        :type config: `dict` or `None`
        """
        # Use the config they provided
        if config is not None:
            self.config = config
        # Use the apps config if `config` was not provided
        elif app is not None:
            self.config = app.config
        self.app = app

        # Setup default config settings
        self.config.setdefault('GRAYLOG_HOST', 'localhost')
        self.config.setdefault('GRAYLOG_PORT', 12201)
        self.config.setdefault('GRAYLOG_FACILITY', 'flask')
        self.config.setdefault('GRAYLOG_EXTRA_FIELDS', True)
        self.config.setdefault('GRAYLOG_ADD_DEBUG_FIELDS', True)
        self.config.setdefault('GRAYLOG_CONFIGURE_MIDDLEWARE', True)

        # Configure the logging handler and attach to this logger
        self.handler = graypy.GELFHandler(
            host=self.config['GRAYLOG_HOST'],
            port=self.config['GRAYLOG_PORT'],
            facility=self.config['GRAYLOG_FACILITY'],
            extra_fields=self.config['GRAYLOG_EXTRA_FIELDS'],
            debugging_fields=self.config['GRAYLOG_ADD_DEBUG_FIELDS'],
        )
        self.addHandler(self.handler)

        # Setup middleware if they asked for it
        if self.config['GRAYLOG_CONFIGURE_MIDDLEWARE']:
            self.setup_middleware()

    def setup_middleware(self):
        """Configure middleware to log each response"""
        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def before_request(self):
        """Middleware handler to record start time of each request"""
        # Record request start time, so we can get response time later
        g.graylog_start_time = time.time()

    def after_request(self, response):
        """Middleware helper to report each flask response to graylog"""
        # Calculate the elapsed time for this request
        elapsed = 0
        if hasattr(g, 'graylog_start_time'):
            elapsed = time.time() - g.graylog_start_time
            elapsed = int(round(1000 * elapsed))

        # Extra metadata to include with the message
        extra = {
            'flask': {
                'endpoint': str(request.endpoint).lower(),
                'view_args': request.view_args,
            },
            'response': {
                'headers': dict(
                    (key.replace('-', '_').lower(), value)
                    for key, value in response.headers
                    if key.lower() not in ('cookie', )
                ),
                'status_code': response.status_code,
                'time_ms': elapsed,
            },
            'request': {
                'content_length': request.environ.get('CONTENT_LENGTH'),
                'content_type': request.environ.get('CONTENT_TYPE'),
                'method': request.environ.get('REQUEST_METHOD'),
                'path_info': request.environ.get('PATH_INFO'),
                'query_string': request.environ.get('QUERY_STRING'),
                'remote_addr': request.environ.get('REMOTE_ADDR'),
                'headers': dict(
                    (key[5:].replace('-', '_').lower(), value)
                    for key, value in request.environ.items()
                    if key.startswith('HTTP_') and key.lower() not in ('http_cookie', )
                )
            },
        }

        message = 'Finishing request for "%s %s" from %s' % (request.method, request.url, extra.get('remote_addr', '-'))
        self.info(message, extra=extra)

        # Always return the response
        return response
