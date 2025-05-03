from datetime import UTC, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UserSchemas:
    """
    This class contains Pydantic schemas for user-related operations.
    """

    class UserBase(BaseModel):
        email: Optional[EmailStr] = None
        phoneNumber: Optional[str] = None
        firstName: Optional[str] = None
        lastName: Optional[str] = None
        password: str = Field(..., min_length=8)

        @field_validator("email", mode="before")
        def blank_email_to_none(cls, v):
            if v == "":
                return None
            return v

    class UserCreate(UserBase):
        roleId: int = 1
        createAt: datetime = Field(default_factory=datetime.now(UTC))
        updateAt: datetime = Field(default_factory=datetime.now(UTC))

    class UserUpdate(UserBase):
        updateAt: datetime = Field(default_factory=datetime.now(UTC))

    class UserInDB(UserBase):
        id: int

    class UserResponse(UserInDB):
        roleId: int = 1
        createAt: datetime = Field(default_factory=datetime.now(UTC))
        updateAt: datetime = Field(default_factory=datetime.now(UTC))

        class Config:
            from_attributes = True  # Chuyển đổi từ SQLAlchemy object thành Pydantic
