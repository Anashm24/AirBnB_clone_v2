#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    # relationship for DBStorage
    cities = relationship("City", backref="state", cascade="all, delete-orphan")

    # getter for FileStorage
    @property
    def cities_list(self):
        """Return a list of cities in the state"""
        from models import storage
        cities_data = storage.all("City").values()
        return [city for city in cities_data if city.state_id == self.id]
