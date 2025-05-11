
from pydantic import BaseModel, Field
from datetime import datetime,timezone
from typing import Optional, List
from app.enums import RoomStatusEnums  # Bạn có thể import từ enum của mình


class RoomSchemas:

    class RoomBase(BaseModel):
        name: str
        price: float
        maxPersonQty: int
        description: str
        status: Optional[str] = (
            RoomStatusEnums.AVAILABLE
        )  # Sử dụng enum cho trạng thái phòng
        # locationId: int

    #     typeRoomId: int

    class RoomCreate(BaseModel):
        name: str
        price: float
        maxPersonQty: int
        description: str
        status: Optional[RoomStatusEnums] = RoomStatusEnums.AVAILABLE
        locationId: int
        # typeRoomId: int

    class RoomUpdate(BaseModel):
        name: Optional[str] = None
        price: Optional[float] = None
        maxPersonQty: Optional[int] = None
        description: Optional[str] = None
        status: Optional[RoomStatusEnums] = RoomStatusEnums.AVAILABLE
        locationId: Optional[int] = None
        # typeRoomId: Optional[int] = None

    class RoomInDB(RoomBase):
        id: int
        create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class RoomResponse(RoomInDB):
        imagePrimary: str
        images: List[str] = None  # Liệt kê hình ảnh của phòng nếu cần

        class Config:
            from_attributes = True
