from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app import schemas
from app import models
from app.crud import RestaurantCRUD
from app.core.auth import get_current_user


class RestaurantAPI:
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["restaurants"])
        self.register_routes()

    def register_routes(self):
        self.router.post("", response_model=schemas.Restaurant)(
            self.create_restaurant
        )
        self.router.post("/menus/", response_model=schemas.Menu)(
            self.upload_menu
        )
        self.router.get("/menus/today/", response_model=List[schemas.Menu])(
            self.get_today_menu
        )

    def create_restaurant(
        self,
        restaurant: schemas.RestaurantCreate,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = RestaurantCRUD(db)
        existing_restaurant = (
            db.query(models.Restaurant)
            .filter(models.Restaurant.name == restaurant.name)
            .first()
        )
        if existing_restaurant:
            raise HTTPException(
                status_code=400,
                detail="Restaurant with this name already registered"
            )
        return crud.create_restaurant(restaurant)

    def upload_menu(
        self,
        menu: schemas.MenuCreate,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = RestaurantCRUD(db)
        restaurant = (
            db.query(models.Restaurant)
            .filter(models.Restaurant.id == menu.restaurant_id)
            .first()
        )
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        existing_menu = (
            db.query(models.Menu)
            .filter(
                models.Menu.restaurant_id == restaurant.id,
                models.Menu.date == menu.date,
            )
            .first()
        )
        if existing_menu:
            raise HTTPException(
                status_code=400,
                detail="Menu already uploaded"
            )
        return crud.create_menu(menu)

    def get_today_menu(
        self,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = RestaurantCRUD(db)
        return crud.get_current_day_menu()


restaurant_api = RestaurantAPI()
router = restaurant_api.router
