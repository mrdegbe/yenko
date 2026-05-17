from fastapi import FastAPI

from app.database import engine, Base

from app.models.rider import Rider
from app.models.ride import Ride

from app.routes.sms import router as sms_router
from app.routes.ussd import router as ussd_router
from app.utils.response import success_response
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Yenko API")


@app.get("/")
def home():

    return success_response("Welcome to Yenko API")


app.include_router(auth_router)
app.include_router(sms_router)
app.include_router(ussd_router)
app.include_router(dashboard_router)
