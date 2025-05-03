from datetime import UTC, datetime
from sqlalchemy import  Column, DateTime, String
from sqlalchemy.orm import relationship
from app.models import BaseModel


class Role(BaseModel):
    __tablename__ = "Roles"
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(50), nullable=False)

    # many to one relationship with user
    user = relationship("User", back_populates="role")

    create_at = Column(DateTime, default=datetime.now(UTC))
    update_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, description={self.description})>"
