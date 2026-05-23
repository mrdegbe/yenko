from pydantic import BaseModel
from typing import Optional


class RideResponse(BaseModel):

    id: int

    customer_phone: str

    pickup_location: str

    destination: str

    fare: Optional[int]

    status: str

    rider_id: Optional[int]

    class Config:

        from_attributes = True
