from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models
from app.core.auth import create_access_token
import bcrypt


class AuthAPI:
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["auth"])
        self.register_routes()

    def register_routes(self):
        self.router.post("")(self.login)

    def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
    ):
        employee = (
            db.query(models.Employee)
            .filter(models.Employee.username == form_data.username)
            .first()
        )
        if not employee or not bcrypt.checkpw(
            form_data.password.encode(), employee.password_hash.encode()
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": employee.username})
        return {"access_token": access_token, "token_type": "bearer"}


auth_api = AuthAPI()
router = auth_api.router
