from pydantic import BaseModel


class DashboardStats(BaseModel):

    total_rides: int

    completed_rides: int

    pending_rides: int

    accepted_rides: int

    total_riders: int

    available_riders: int

    total_revenue: int
