Flask-Graylog
=============

This is a [Flask](http://flask.pocoo.org/) extension that allows you to configure a [Graylog](https://graylog.org/) log handler as well as configuring middleware to log every request/response to Graylog.


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
