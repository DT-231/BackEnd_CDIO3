from datetime import date, timedelta
from typing import List, Optional
from fastapi import Depends, Request, status
from fastapi.params import Body, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.databases import get_db
from app.enums import RoomStatusEnums
from app.schemas import LocationSchemas, RoomSchemas
from app.services.ImageService import addImages
from app.services.LocationService import createNewLocation
from app.services.RoomService import (
    checkRoomExist,
    createNewRoom,
    getRoomById,
    searchRoom,
)


async def HandleSearchRooms(
    request: Request,
    searchLocation: str = Query(...),
    person_qty: int = Query(1),
    check_in: date = Query(date.today()),
    check_out: date = Query(date.today() + timedelta(days=1)),
    type_search: Optional[str] = Query("less"),  # Sửa cú pháp này
    price_min: Optional[int] = Query(None),
    price_max: Optional[int] = Query(None),
    page: int = Query(1),
    items_per_page: Optional[int] = Query(5),
    sort_by: Optional[str] = Query(
        "price_asc"
    ),  # price_asc : Thấp đến cao / thấp nhất  hoặc price_desc : cao nhất / cao đến thấp
    db: Session = Depends(get_db),
):
    try:
        # Validate input ccheck-in date must be before check-out
        if check_in >= check_out:
            return JSONResponse(
                status_code=400,
                content={
                    "code": 1,
                    "message": "Ngày check-in phải nhỏ hơn ngày check-out.",
                    "data": "",
                },
            )

        # The date of check-in and check-out cannot be in the past
        if check_in < date.today() or check_out < date.today():
            return JSONResponse(
                status_code=400,
                content={
                    "code": 1,
                    "message": "Ngày check-in và check-out không được nhỏ hơn ngày hiện tại.",
                    "data": "",
                },
            )
        # Validate person_qty must be greater than 0
        if person_qty <= 0:
            return JSONResponse(
                status_code=400,
                content={
                    "code": 1,
                    "message": "Số lượng người không được nhỏ hơn hoặc bằng 0.",
                    "data": "",
                },
            )

        # check type search  , if less  then set items_per_page to 5 and page to 1
        if type_search not in ["less", "more"]:
            return JSONResponse(
                status_code=400,
                content={
                    "code": 1,
                    "message": "type_search không hợp lệ. Chỉ chấp nhận less hoặc more.",
                    "data": "",
                },
            )
        if type_search == "less":
            items_per_page = 5
            page = 1

        response = searchRoom(
            db=db,
            searchLocation=searchLocation,
            check_in=check_in,
            check_out=check_out,
            price_min=price_min,
            price_max=price_max,
            person_qty=person_qty,
            page=page,
            items_per_page=items_per_page,
            sort_by=sort_by,
        )

        return response

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 1,
                "message": str(e),
                "data": "",
            },
        )


async def HandleReadRoomDetail(
    request: Request,
    roomId: int = Query(...),
    db: Session = Depends(get_db),
):
    try:
        if not roomId and not roomId.is_digit():
            return JSONResponse(
                status_code=400,
                content={
                    "code": 1,
                    "message": "roomId không hợp lệ.",
                    "data": "",
                },
            )

        res = getRoomById(roomId, db)
        return res
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 1,
                "message": str(e),
                "data": "",
            },
        )


async def HandleCreateRoom(
    request: Request,
    name: str = Body(...),
    price: float = Body(...),
    maxPersonQty: int = Body(...),
    description_hotel: str = Body(...),
    status: Optional[str] = Body(RoomStatusEnums.AVAILABLE),
    address: str = Body(...),
    district: str = Body(...),
    city: str = Body(...),
    country: str = Body(...),
    description_location: str = Body(...),
    imagesRoom: List[str] = Body(...),
    db: Session = Depends(get_db),
):
    try:
        if price == 0 or maxPersonQty < 1:
            return JSONResponse(
                status_code=400,
                content={
                    "code": 1,
                    "message": "Price must be greater than 0 and max person quantity must be at least 1",
                    "data": "",
                },
            )

        # Bọc toàn bộ logic trong transaction
        with db.begin():
            location = LocationSchemas.locationCreate(
                address=address,
                district=district,
                city=city,
                country=country,
                description=description_location,
            )

            # Tạo mới vị trí
            resultLocation = createNewLocation(location=location, db=db)
            if not resultLocation:
                raise Exception("Failed to create location")
            room = RoomSchemas.RoomCreate(
                name=name,
                price=price,
                maxPersonQty=maxPersonQty,
                description=description_hotel,
                status=status,
                locationId=resultLocation,
                imagesRoom=imagesRoom,
            )

            # kiểm tra phòng đã tồn tại hay chưa
            check = checkRoomExist(room.name, room.locationId, db)
            if not check:
                raise Exception("Phòng đã tồn tại")

            # tạo phòng mới và trả về id
            roomId = createNewRoom(room=room, db=db)
            if not roomId:
                raise Exception("Failed to create room")
            # thêm ảnh của phòng
            success = addImages(imagesRoom, roomId, db)

            if not success:
                raise Exception("Failed to add images")

            db.commit()

        # Commit tự động khi thoát with (nếu không lỗi)
        return JSONResponse(
            status_code=201,
            content={
                "code": 0,
                "message": "Tạo phòng thành công",
                "data": "",
            },
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 1,
                "message": str(e),
                "data": "",
            },
        )
