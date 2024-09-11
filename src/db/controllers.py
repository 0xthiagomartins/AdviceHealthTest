from sqlmodel_controller import Controller
from .models import Person, Car
from .database import engine


class Controllers:
    def __init__(self):
        self.person = Controller[Person](engine=engine)
        self.car = Controller[Car](engine=engine)


controllers = Controllers()
