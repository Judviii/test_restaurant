from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api import restaurant, auth, employee, vote
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/token", tags=["auth"])
app.include_router(
    restaurant.router, prefix="/restaurants", tags=["restaurants"]
)
app.include_router(employee.router, prefix="/employees", tags=["employees"])
app.include_router(vote.router, prefix="/votes", tags=["votes"])


@app.middleware("http")
async def check_app_version(request: Request, call_next):
    app_version = request.headers.get("App-Version", "2.0")
    allowed_versions = {"1.0", "2.0"}
    if app_version not in allowed_versions:
        msg = f"Unsupported app version: {app_version}. "
        msg += f"Supported versions: {', '.join(allowed_versions)}"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": msg,
            },
        )
    request.state.app_version = app_version
    response = await call_next(request)
    return response
