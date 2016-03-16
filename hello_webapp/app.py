import sys, traceback, os

from flask import Flask, render_template, send_from_directory

from hello_webapp.settings import PROJECT_PATH, LOCAL
from hello_webapp.helpers import _log


# paths
FLASK_DIR = os.path.join(PROJECT_PATH, 'hello_webapp')
TEMPLATE_DIR = os.path.join(FLASK_DIR, 'templates')
STATIC_DIR = os.path.join(FLASK_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=PROJECT_PATH)
app.debug = LOCAL


@app.route("/")
def hello():
    return render_template("hello.html")


@app.route('/static/<path:path>')
def send_static(path):
    """
    for local static serving
    this route will never be reached on the server because nginx will bypass flask all together
    """
    return send_from_directory(STATIC_DIR, path)


@app.errorhandler(500)
def error_handler_500(e):
    """
    if a page throws an error, log the error to slack, and then re-raise the error
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    formatted_lines = traceback.format_exc()
    _log('@channel: 500 error: {}'.format(e.message))
    _log(formatted_lines)
    raise e


@app.route('/error/')
def flask_force_error():
    """
    this helper page forces an error, for testing error logging
    """
    raise Exception('forced 500 error')


@app.route('/slack/')
def flask_slack_test():
    """
    this helper page for testing if slack is working
    """
    _log('@channel: slack is working?')
    return 'slack test'


if __name__ == "__main__":
    app.run()
