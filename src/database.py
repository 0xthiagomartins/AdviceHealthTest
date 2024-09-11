from sqlmodel_controller import Controller
from src.models import Person, Car

person_controller = Controller[Person]()
car_controller = Controller[Car]()


def init_db():
    # The database will be automatically initialized when the controllers are created
    pass
