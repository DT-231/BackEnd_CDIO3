from datetime import UTC, datetime
from sqlalchemy import DATE, Column, DateTime, Double, Integer, String
from sqlalchemy.orm import relationship

from app.models import BaseModel


class TypeRoom(BaseModel):
    __tablename__ = "TypeRooms"

    name = Column(String(50), nullable=False)
    maxOccupancy = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)

    room = relationship("Room", back_populates="typeRoom")
    
    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
