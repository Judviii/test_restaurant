from pydantic import BaseModel
from datetime import date


class RestaurantBase(BaseModel):
    name: str


class RestaurantCreate(RestaurantBase):
    pass


class Restaurant(RestaurantBase):
    id: int

    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    restaurant_id: int
    date: date
    items: str


class MenuCreate(MenuBase):
    pass


class Menu(MenuBase):
    id: int

    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    username: str


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class VoteBase(BaseModel):
    menu_id: int
    date: date


class VoteCreate(VoteBase):
    pass


class Vote(VoteBase):
    id: int

    class Config:
        from_attributes = True
