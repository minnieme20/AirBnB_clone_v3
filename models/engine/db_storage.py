#!/usr/bin/python3
"""
    defines a DataBaseStorage
"""
import models
from models.base_model import Base
from models.city import City
from models.state import State
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv("HBNB_MYSQ_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """querry current database session"""
        db_dict = {}

        if cls is not None and cls != '':
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    objs = self.__session.query(v).all()
                    if len(objs) > 0:
                        for obj in objs:
                            key = "{}.{}".format(obj.__class__.__name__,
                                                 obj.id)
                            db_dict[key] = obj
            return db_dict

    def new(self, obj):
        """add obj to current database"""
        self.__session.add(obj)

    def save(self):
        """commits the changes on the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload current database"""
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """remove private session attribute"""
        self.__session.close()

    def get(self, cls, id):
        """A method to retrieve one object
        """
        obj_dict = models.storage.ll(cls)
        for k, v in obj_dict.items():
            matchstring = cls + '.' + id
            if k == matchstring:
                return v
        return None

    def count(self, cls=None):
        """Returns the number of objects in storage matching the given class"""
        obj_dict = models.storage.all(cls)
        return len(obj_dict)
