from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.ride import Ride

from app.models.rider import Rider

from app.schemas.dashboard import DashboardResponse, DashboardStats

from app.auth.dependencies import get_current_admin
from app.utils.response import success_response

router = APIRouter()


@router.get("/dashboard/stats", response_model=DashboardResponse)
def dashboard_stats(
    current_admin=Depends(get_current_admin), db: Session = Depends(get_db)
):

    rides = db.query(Ride).all()

    riders = db.query(Rider).all()

    completed_rides = [ride for ride in rides if ride.status == "completed"]

    pending_rides = [ride for ride in rides if ride.status == "pending"]

    accepted_rides = [ride for ride in rides if ride.status == "accepted"]

    available_riders = [rider for rider in riders if rider.is_available]

    total_revenue = sum(ride.fare or 0 for ride in completed_rides)

    return success_response(
        "Dashboard stats",
        {
            "total_rides": len(rides),
            "completed_rides": len(completed_rides),
            "pending_rides": len(pending_rides),
            "accepted_rides": len(accepted_rides),
            "total_riders": len(riders),
            "available_riders": len(available_riders),
            "total_revenue": total_revenue,
        },
    )

    # return DashboardStats(
    #     total_rides=len(rides),
    #     completed_rides=len(completed_rides),
    #     pending_rides=len(pending_rides),
    #     accepted_rides=len(accepted_rides),
    #     total_riders=len(riders),
    #     available_riders=len(available_riders),
    #     total_revenue=total_revenue,
    # )
