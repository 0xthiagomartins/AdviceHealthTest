from sqlmodel import Field, Relationship
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
    cars: list["Car"] = Relationship(
        back_populates="owner",
    )


class Car(BaseID, table=True):
    color: CarColor
    model: CarModel
    owner_id: int = Field(foreign_key="person.id")
    owner: Person = Relationship(back_populates="cars")
