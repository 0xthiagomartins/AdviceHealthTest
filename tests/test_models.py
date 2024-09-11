import pytest
from src.db.models import Person, Car, CarColor, CarModel


def test_person_model():
    person = Person(name="John Doe")
    assert person.name == "John Doe"
    assert person.cars == []


def test_car_model():
    car = Car(color=CarColor.BLUE, model=CarModel.SEDAN, owner_id=1)
    assert car.color == CarColor.BLUE
    assert car.model == CarModel.SEDAN
    assert car.owner_id == 1


def test_car_color_enum():
    assert CarColor.YELLOW.value == "yellow"
    assert CarColor.BLUE.value == "blue"
    assert CarColor.GRAY.value == "gray"


def test_car_model_enum():
    assert CarModel.HATCH.value == "hatch"
    assert CarModel.SEDAN.value == "sedan"
    assert CarModel.CONVERTIBLE.value == "convertible"
