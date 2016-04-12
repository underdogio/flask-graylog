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

    from flask import Flask
    from flask.ext.graylog import Graylog

    app = Flask(__name__)
    graylog = Graylog(app)
