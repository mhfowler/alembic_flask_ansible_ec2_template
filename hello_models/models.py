from sqlalchemy import Column, Integer, String
from hello_models.database import Base


class TestObject(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)
