from datetime import UTC, datetime
import dis
from sqlalchemy import DATE, Column, DateTime, String
from app.models import BaseModel
from sqlalchemy.orm import relationship


class Location(BaseModel):
    __tablename__ = "Locations"

    address = Column(String(100))  # Location room /địa chỉ phòng
    district = Column(String(50))  # district / quận huyện
    city = Column(String(50))  # city / thành phố
    country = Column(String(50))  # country / quốc gia
    description = Column(String(255))  # description of Location / mô tả địa điểm

    # one to many relationship with room
    rooms = relationship(
        "Room", back_populates="location"
    )  # Changed to plural 'rooms' and lowercase 'location'

    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
