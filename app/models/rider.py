from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Rider(Base):

    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String, unique=True)

    location = Column(String)

    is_available = Column(Boolean, default=True)

    status = Column(String, default="offline")
