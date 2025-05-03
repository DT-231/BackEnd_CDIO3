from datetime import UTC, datetime
from pydantic import BaseModel, Field


class RoleSchemas:

    class RoleBase(BaseModel):
        name: str
        description: str

    class RoleCreate(RoleBase):
        createAt: datetime = Field(default_factory=lambda: datetime.now(UTC))
        updateAt: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class RoleResponse(RoleBase):
        id: int
        createAt: datetime = Field(default_factory=lambda: datetime.now(UTC))
        updateAt: datetime = Field(default_factory=lambda: datetime.now(UTC))

        class Config:
            from_attributes = True  # Chuyển đổi từ SQLAlchemy object thành Pydantic
