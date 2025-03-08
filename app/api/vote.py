from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.db.database import get_db
from app import schemas
from app import models
from app.crud import VoteCRUD
from app.core.auth import get_current_user


class VoteAPI:
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["votes"])
        self.register_routes()

    def register_routes(self):
        self.router.post("", response_model=schemas.Vote)(self.create_new_vote)
        self.router.get("/today/", response_model=List[schemas.Vote])(
            self.get_today_votes
        )
        self.router.get("/results/today/")(self.get_today_results)

    def create_new_vote(
        self,
        vote: schemas.VoteCreate,
        request: Request,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = VoteCRUD(db, current_user)
        app_version = request.state.app_version
        # Just for example, we are checking the app version here and we can add
        # different logic, but the application should work on 2 versions,
        # older and younger so middlaware intercepts the version and allows you
        # to work with 2 versions in exactly the same way.
        # But if necessary, you can add different logic for different versions
        if app_version == "1.0":
            # print("App version 1.0")
            pass
        if app_version == "2.0":
            # print("App version 2.0")
            pass

        try:
            return crud.create_vote(vote)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_today_votes(
        self,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = VoteCRUD(db, current_user)
        today = date.today()
        return crud.get_votes_by_date(today)

    def get_today_results(
        self,
        db: Session = Depends(get_db),
        current_user: models.Employee = Depends(get_current_user),
    ):
        crud = VoteCRUD(db, current_user)
        today = date.today()
        return crud.get_vote_results(today)


vote_api = VoteAPI()
router = vote_api.router
