import logging
import time

from flask import g, request
import graypy


class Graylog(logging.Logger):
    def __init__(self, app=None, config=None, level=logging.NOTSET):
        super(Graylog, self).__init__(__name__, level=level)

        if app is not None or config is not None:
            self.init_app(app, config)

    def init_app(self, app=None, config=None):
        self.config = config
        if config is None and app is not None:
            self.config = app.config
        self.app = app

        self.config.setdefault('GRAYLOG_HOST', 'localhost')
        self.config.setdefault('GRAYLOG_PORT', 12201)
        self.config.setdefault('GRAYLOG_FACILITY', 'flask')
        self.config.setdefault('GRAYLOG_EXTRA_FIELDS', None)
        self.config.setdefault('GRAYLOG_ADD_DEBUG_FIELDS', True)

        graypy_handler = graypy.GELFHandler(
            host=self.config['GRAYLOG_HOST'],
            port=self.config['GRAYLOG_PORT'],
            facility=self.config['GRAYLOG_FACILITY'],
            extra_fields=self.config['GRAYLOG_EXTRA_FIELDS'],
            debugging_fields=self.config['GRAYLOG_ADD_DEBUG_FIELDS'],
        )
        self.addHandler(graypy_handler)

        self.app.before_request(self.before_request)
        self.app.after_request(self.after_request)

    def before_request(self):
        g.graylog_start_time = time.time()
        self.debug('Handling request for "%s %s" from %s' %
                   (request.method, request.url, request.environ.get('REMOTE_ADDR', '-')))

    def after_request(self, response):
        elapsed = 0
        if hasattr(g, 'graylog_start_time'):
            elapsed = time.time() - g.graylog_start_time
            elapsed = int(round(1000 * elapsed))

        extra = {
            'endpoint': str(request.endpoint).lower(),
            'status_code': response.status_code,
            'response_time_ms': elapsed,
            'view_args': request.view_args,
        }

        for key, value in response.headers:
            key = 'response_http_%s' % (key.replace('-', '_').lower(), )
            extra[key] = value

        for key, value in request.environ.iteritems():
            extra[key.lower()] = value

        message = 'Finishing request for "%s %s" from %s' % (request.method, request.url, extra.get('remote_addr', '-'))
        self.info(message, extra=extra)

        # Always return the response
        return response
