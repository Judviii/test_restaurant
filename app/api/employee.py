from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import schemas
from app import models
from app.crud import EmployeeCRUD
from app.core.auth import get_current_user


class EmployeeAPI:
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["employees"])
        self.register_routes()

    def register_routes(self):
        self.router.post("", response_model=schemas.Employee)(
            self.create_new_employee
        )
        self.router.get("/{employee_id}/", response_model=schemas.Employee)(
            self.read_employee
        )

    def create_new_employee(
        self, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)
    ):
        crud = EmployeeCRUD(db)
        try:
            return crud.create_employee(employee)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def read_employee(
        self,
        employee_id: int,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = EmployeeCRUD(db)
        db_employee = crud.get_employee(employee_id)
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return db_employee


employee_api = EmployeeAPI()
router = employee_api.router
