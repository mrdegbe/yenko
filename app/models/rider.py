from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Rider(Base):

    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String, unique=True)

    location = Column(String)

    is_available = Column(Boolean, default=True)

    # status = Column(String, default="offline")
    status = Column(String, default="offline")

    earnings = Column(Integer, default=0)

    rides = relationship("Ride", back_populates="rider")
