from flask import Flask
from flask.ext.graylog import Graylog

app = Flask(__name__)
graylog = Graylog(app)


@app.route('/')
def root():
    return 'thanks'


if __name__ == '__main__':
    app.debug = True
    app.run()
