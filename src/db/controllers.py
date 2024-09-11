from sqlmodel_controller import Controller
from .models import Person, Car
from sqlmodel import create_engine


def get_engine():
    db_uri = f"sqlite:///./carford.db"
    return create_engine(db_uri)


class Controllers:
    def __init__(self):
        engine = get_engine()
        self.person = Controller[Person](engine=engine)
        self.car = Controller[Car](engine=engine)


controllers = Controllers()
