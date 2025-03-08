from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    menus = relationship("Menu", back_populates="restaurant")


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    date = Column(Date, index=True)
    items = Column(String)
    restaurant = relationship("Restaurant", back_populates="menus")
    votes = relationship("Vote", back_populates="menu")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    votes = relationship("Vote", back_populates="employee")


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    menu_id = Column(Integer, ForeignKey("menus.id"))
    date = Column(Date, index=True)
    employee = relationship("Employee", back_populates="votes")
    menu = relationship("Menu", back_populates="votes")
