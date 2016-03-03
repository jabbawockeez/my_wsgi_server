# sqlalchemy import
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config


class DataBase:

    def __init__(self, engine_url, **kwargs):
        self.engine = create_engine(
            engine_url, **kwargs)
        self.Model = declarative_base()
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """create tables in database"""
        self.Model.metadata.create_all(self.engine)

db = DataBase(
    config.DATABASE_URI,
    echo=config.DATABASE_ECHO,
    pool_recycle=5
)
