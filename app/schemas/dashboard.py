from pydantic import BaseModel
from app.schemas.common import ApiResponse


class DashboardStats(BaseModel):

    total_rides: int

    completed_rides: int

    pending_rides: int

    accepted_rides: int

    total_riders: int

    available_riders: int

    total_revenue: int




class DashboardResponse(ApiResponse):

    data: DashboardStats