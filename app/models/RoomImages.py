
from datetime import datetime,UTC
from sqlalchemy.orm import relationship
from sqlalchemy import DATE, Boolean, Column, DateTime, ForeignKey, Integer, String
from app.models import BaseModel


class RoomImage(BaseModel):
    __tablename__ = "RoomImages"

    roomId = Column(Integer, ForeignKey("Rooms.id"))
    room = relationship("Room", back_populates="images")

    url = Column(String(255), nullable=False)
    isPrimary = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))