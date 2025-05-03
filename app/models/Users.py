from datetime import UTC, datetime

from sqlalchemy import DATE, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import BaseModel


class User(BaseModel):
    __tablename__ = "Users"
    email = Column(String(50), nullable=True, unique=True)
    phoneNumber = Column(String(12), nullable=True, unique=True)

    password = Column(String(255), nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)

    roleId = Column(Integer, ForeignKey("Roles.id"))
    role = relationship("Role", back_populates="user")

    booking = relationship("Booking", back_populates="user")

    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, phoneNumber={self.phoneNumber}, firstName={self.firstName}, lastName={self.lastName})>"
