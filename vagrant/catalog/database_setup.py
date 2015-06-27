import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class CatalogItem(Base):
    __tablename__ = "catalog_item"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String(250))
    catalog_id = Column(Integer, ForeignKey("catalog.id"))
    catalog = relationship(Catalog)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "price": self.price,
            "course": self.course
        }


engine = create_engine("sqlite:///catalog.db")


Base.metadata.create_all(engine)
