from datetime import UTC, datetime
from sqlalchemy import (
    Column,
    DateTime,
    Double,
    ForeignKey,
    Integer,
    String,
    Text,
)
from app.enums import RoomStatusEnums
from app.models import BaseModel
from sqlalchemy.orm import relationship


class Room(BaseModel):
    __tablename__ = "Rooms"
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Double, nullable=False)
    maxPersonQty = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    status = Column(String(15), default=RoomStatusEnums.AVAILABLE)

    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    # relationship

    # many to one relationship with location
    locationId = Column(Integer, ForeignKey("Locations.id"))
    location = relationship("Location", back_populates="rooms")

    # one to many relationship with room_images
    images = relationship("RoomImage", back_populates="room")

    #
    # typeRoomId = Column(Integer, ForeignKey("TypeRooms.id"))
    # typeRoom = relationship("TypeRoom", back_populates="room")

    # many to one relationship with booking
    booking = relationship("Booking", back_populates="room")
