#!/usr/bin/python3
"""represent a database storage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """represent a new engine"""
    __engine = None
    __session = None
    
    def __init__(self):
        db_config = {
            'user': getenv('HBNB_MYSQL_USER'),
            'password': getenv('HBNB_MYSQL_PWD'),
            'host': getenv('HBNB_MYSQL_HOST'),
            'db': getenv('HBNB_MYSQL_DB')
        }
        self.__engine = create_engine(
            f"mysql+mysqldb://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}/{db_config['db']}",
            pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objects = self.__session.query(State).all()
            objects.extend(self.__session.query(City).all())
            objects.extend(self.__session.query(User).all())
            objects.extend(self.__session.query(Place).all())
            objects.extend(self.__session.query(Review).all())
            objects.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objects = self.__session.query(cls).all()
        return {f"{type(obj).__name__}.{obj.id}": obj for obj in objects}

    def new(self, obj):
        """add the object to the current 
        database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current 
        database session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """Delete an object from the session if provided."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database engine and reset the session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__engine = Session()
