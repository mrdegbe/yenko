from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from datetime import datetime, timedelta

from app.database import Base


class Ride(Base):

    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)

    customer_phone = Column(String)

    pickup = Column(String)

    destination = Column(String)

    status = Column(String, default="pending")

    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    accepted_at = Column(DateTime, nullable=True)

    completed_at = Column(DateTime, nullable=True)

    expires_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(seconds=60)
    )
    fare = Column(Integer, nullable=True)
