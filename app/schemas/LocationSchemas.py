from datetime import datetime 
from typing import Optional
from pydantic import BaseModel


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
        create_at: datetime
        update_at: datetime

        class Config:
            from_attributes = True
