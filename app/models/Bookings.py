from ast import In
from datetime import datetime, UTC
from sqlalchemy import  Column, Date, DateTime, ForeignKey, Integer, String
from app.enums import  BookingStatusEnums
from app.models import BaseModel
from sqlalchemy.orm import relationship


class Booking(BaseModel):
    __tablename__ = "bookings"

    # User ID of the user who made the booking
    userId = Column(Integer, ForeignKey("Users.id"), nullable=False)
    #  one to many relationship with the User model
    user = relationship("User", back_populates="booking")

    # Room ID of the room being booked
    roomId = Column(Integer, ForeignKey("Rooms.id"), nullable=False)
    # one to many relationship with the Room model
    room = relationship("Room", back_populates="booking")

    # Check-in date for the booking
    checkIn = Column(Date, nullable=False)
    # Check-out date for the booking
    checkOut = Column(Date, nullable=False)

    status = Column(String(15), default=BookingStatusEnums.PENDING, nullable=False)

    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    def __repr__(self):
        return f"<Booking(id={self.id}, userId={self.userId}, roomId={self.roomId}, checkIn={self.checkIn}, checkOut={self.checkOut}, status={self.status})>"
