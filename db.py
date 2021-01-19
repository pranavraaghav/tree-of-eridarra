from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String

# DB Set up
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Models
class Encouragement(Base):
    __tablename__='encouragements'

    def __init__(self, phrase):
        self.phrase=phrase

    phrase=Column(String, primary_key=True)

# Creating Schema
Base.metadata.create_all(engine)

# Operations
def add(item):
    session.merge(item)
    session.commit()

def delete(item):
    session.delete(item)
    session.commit()

def get_all(type):
    return session.query(type)

## Testing
# temp = Encouragement(phrase='Be good')
# add(temp)

# answer = session.query(type(temp)).all()
# for x in answer:
#     print(x.phrase)
