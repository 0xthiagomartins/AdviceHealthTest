from sqlmodel import Field
from sqlmodel_controller import BaseID
from enum import Enum


class CarColor(str, Enum):
    YELLOW = "yellow"
    BLUE = "blue"
    GRAY = "gray"


class CarModel(str, Enum):
    HATCH = "hatch"
    SEDAN = "sedan"
    CONVERTIBLE = "convertible"


class Person(BaseID, table=True):
    name: str
    cars: list["Car"] = []


class Car(BaseID, table=True):
    color: CarColor
    model: CarModel
    owner_id: int = Field(foreign_key="person.id")
    owner: Person = None
