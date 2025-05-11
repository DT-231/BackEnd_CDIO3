from datetime import datetime ,timezone
from typing import Optional
from pydantic import BaseModel, Field


class LocationSchemas:

    # class locationBase(BaseModel):

    class locationCreate(BaseModel):
        address: str
        district: Optional[str] = None
        city: str
        country: str
        description: Optional[str] = None

    class locationUpadte(BaseModel):
        address: Optional[str] = None
        district: Optional[str] = None
        city: Optional[str] = None
        country: Optional[str] = None
        description: Optional[str] = None

    # class locationInDB(locationCreate):

    class locationResponse(locationCreate):
        id: int
        create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

        class Config:
            from_attributes = True
