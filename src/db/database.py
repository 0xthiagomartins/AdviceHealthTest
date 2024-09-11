from sqlmodel import SQLModel, create_engine
from src.db.models import Person, Car  # Import your models here

DATABASE_URL = "sqlite:///./carford.db"

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
