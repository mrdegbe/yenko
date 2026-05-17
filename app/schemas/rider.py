from pydantic import BaseModel


class RiderResponse(BaseModel):

    id: int

    name: str

    phone: str

    location: str

    status: str

    is_available: bool

    earnings: int

    class Config:

        from_attributes = True
