from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from datetime import datetime, timedelta

from app.constants.ride_status import *
from app.database import Base

from sqlalchemy.orm import relationship


class Ride(Base):

    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)

    customer_phone = Column(String)

    pickup_location = Column(String)

    destination = Column(String)

    status = Column(String, default=PENDING)

    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    accepted_at = Column(DateTime, nullable=True)

    completed_at = Column(DateTime, nullable=True)

    expires_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(seconds=60)
    )
    fare = Column(Integer, nullable=True)

    rider = relationship("Rider", back_populates="rides")
