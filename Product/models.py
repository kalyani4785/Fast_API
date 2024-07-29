from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

# Creating database models 
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    # Foreign key
    seller_id = Column(Integer, ForeignKey('sellers.id'))
    # creating relationship between each other()
    seller = relationship("Seller", back_populates='products')


class Seller(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    # creating relationship between each other
    products = relationship("Product", back_populates='seller')

