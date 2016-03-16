from flask import render_template
from flask import Blueprint

from hello_webapp.helpers import _log
from hello_webapp.test import get_test_objects, create_test_object


def get_hello_helpers_blueprint(db, template_dir):

    # blueprint for these routes
    hello_helpers = Blueprint('hello_helpers', __name__, template_folder=template_dir)

    @hello_helpers.route('/error/')
    def flask_force_error():
        """
        this helper page forces an error, for testing error logging
        """
        raise Exception('forced 500 error')

    @hello_helpers.route('/slack/')
    def flask_slack_test():
        """
        this helper page for testing if slack is working
        """
        _log('@channel: slack is working?')
        return 'slack test'

    @hello_helpers.route('/test_db/')
    def test_db_page():
        """
        this helper page confirms that the database is connected and working
        :return:
        """
        create_test_object(db)
        test_objects = get_test_objects(db)
        return render_template("hello_db.html", test_objects=test_objects)

    # finally return blueprint
    return hello_helpers

