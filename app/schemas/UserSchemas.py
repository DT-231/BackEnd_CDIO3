from datetime import UTC, datetime, timezone
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UserSchemas:
    """
    This class contains Pydantic schemas for user-related operations.
    """

    class UserBase(BaseModel):
        email: Optional[str] = None
        phoneNumber: Optional[str] = None
        firstName: Optional[str] = None
        lastName: Optional[str] = None
        password: str = Field(..., min_length=8)

    class UserCreate(UserBase):
        roleId: int = 1
        createAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        updateAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class UserUpdate(UserBase):
        updateAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class UserInDB(UserBase):
        id: int

    class UserResponse(UserInDB):
        roleId: int = 1
        createAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        updateAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

        class Config:
            from_attributes = True  # Chuyển đổi từ SQLAlchemy object thành Pydantic
