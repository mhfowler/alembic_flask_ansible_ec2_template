from hello_models.database import db_session
from hello_models.models import TestObject


def create_test_object():
    u = TestObject(name='admin', email='admin@localhost')
    db_session.add(u)
    db_session.commit()


def get_test_objects():
    users = TestObject.query.all()
    for u in users:
        print u.email


if __name__ == '__main__':
    create_test_object()
    # get_test_objects()