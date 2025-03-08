import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List, Dict, Any
from app import models
from app import schemas


class RestaurantCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_restaurant(self, restaurant: schemas.RestaurantCreate):
        db_restaurant = models.Restaurant(name=restaurant.name)
        self.db.add(db_restaurant)
        self.db.commit()
        self.db.refresh(db_restaurant)
        return db_restaurant

    def create_menu(self, menu: schemas.MenuCreate) -> models.Menu:
        db_menu = models.Menu(**menu.dict())
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu

    def get_current_day_menu(self) -> List[models.Menu]:
        today = date.today()
        return self.db.query(
            models.Menu
        ).filter(models.Menu.date == today).all()


class EmployeeCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_employee(
        self, employee: schemas.EmployeeCreate
    ) -> models.Employee:
        existing_employee = (
            self.db.query(models.Employee)
            .filter(models.Employee.username == employee.username)
            .first()
        )
        if existing_employee:
            raise ValueError("Username already registered")
        password_hash = bcrypt.hashpw(
            employee.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        db_employee = models.Employee(
            username=employee.username, password_hash=password_hash
        )
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def get_employee(self, employee_id: int) -> models.Employee | None:
        return (
            self.db.query(models.Employee)
            .filter(models.Employee.id == employee_id)
            .first()
        )


class VoteCRUD:
    def __init__(self, db: Session, current_user: models.Employee):
        self.db = db
        self.current_user = current_user

    def create_vote(self, vote: schemas.VoteCreate) -> models.Vote:
        existing_vote = (
            self.db.query(models.Vote)
            .filter(
                models.Vote.employee_id == self.current_user.id,
                models.Vote.date == vote.date,
            )
            .first()
        )
        if existing_vote:
            raise ValueError("Employee has already voted today")

        menu = self.db.query(
            models.Menu
        ).filter(models.Menu.id == vote.menu_id).first()
        if not menu:
            raise ValueError("Menu not found")

        db_vote = models.Vote(
            employee_id=self.current_user.id,
            menu_id=vote.menu_id,
            date=vote.date
        )
        self.db.add(db_vote)
        self.db.commit()
        self.db.refresh(db_vote)
        return db_vote

    def get_votes_by_date(self, vote_date: date) -> List[models.Vote]:
        return self.db.query(
            models.Vote
        ).filter(models.Vote.date == vote_date).all()

    def get_vote_results(self, vote_date: date) -> List[Dict[str, Any]]:
        results = (
            self.db.query(
                models.Menu,
                func.count(models.Vote.id).label("vote_count")
            )
            .outerjoin(models.Vote, models.Vote.menu_id == models.Menu.id)
            .filter(models.Menu.date == vote_date)
            .group_by(models.Menu.id)
            .all()
        )
        return [
            {
                "menu": menu,
                "vote_count": vote_count
            } for menu, vote_count in results
        ]
