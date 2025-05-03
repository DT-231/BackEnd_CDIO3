from datetime import date
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models import Booking, Location, Room, RoomImage
from sqlalchemy.orm import Session
from sqlalchemy import or_, select, and_, func

from app.schemas import LocationSchemas, RoleSchemas, RoomSchemas


def getAllRooms(db: Session):
    try:
        role_raw = db.query(Room).all()
        if not role_raw:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "code": 1,
                    "message": "No roles found",
                    "data": "",
                },
            )
        rolesResponse = [
            RoleSchemas.RoleResponse.from_orm(role).model_dump() for role in role_raw
        ]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 0,
                "message": "Roles retrieved successfully",
                "data": jsonable_encoder(rolesResponse),
            },
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 1,
                "message": "Internal server error",
                "data": "",
            },
        )


def searchRoom(
    db: Session,
    searchLocation: str,
    check_in: date,
    check_out: date,
    price_min: float = None,
    price_max: float = None,
    person_qty: int = 1,
    page: int = 1,
    items_per_page: int = 5,
    sort_by: str = "price_asc",
):
    try:
        # Create a proper select statement for the subquery
        booked_rooms_select = (
            select(Booking.roomId)
            .where(and_(Booking.checkIn < check_out, Booking.checkOut > check_in))
            .distinct()
        )

        # Normalize the search term by removing extra spaces and converting to lowercase
        normalized_search = " ".join(searchLocation.lower().split())

        # Base query for available rooms
        query = (
            db.query(Room)
            .join(Location, Location.id == Room.locationId)
            .filter(
                Room.id.not_in(booked_rooms_select),
                Room.maxPersonQty >= person_qty,
            )
        )

        # Apply the search filter with multiple conditions for more flexible matching
        query = query.filter(
            or_(
                func.lower(Location.address).contains(normalized_search),
                func.lower(Location.city).contains(normalized_search),
                func.lower(Location.district).contains(normalized_search),
                func.lower(Location.country).contains(normalized_search),
                func.lower(Room.name).contains(normalized_search),
                # Handle case where spaces might be different in the search term
                func.lower(Room.name).contains(normalized_search.replace(" ", "")),
                # Also try with spaces completely removed from search term
                func.replace(func.lower(Room.name), " ", "").contains(
                    normalized_search.replace(" ", "")
                ),
            )
        )

        # Apply price filters
        if price_min is not None:
            query = query.filter(Room.price >= float(price_min))

        if price_max is not None:
            query = query.filter(Room.price <= float(price_max))

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        if sort_by == "price_asc":
            rooms = (
                query.order_by(Room.price.asc())
                .limit(items_per_page)
                .offset((page - 1) * items_per_page)
                .all()
            )
        elif sort_by == "price_desc":
            rooms = (
                query.order_by(Room.price.desc())
                .limit(items_per_page)
                .offset((page - 1) * items_per_page)
                .all()
            )
        else:
            rooms = (
                query.limit(items_per_page).offset((page - 1) * items_per_page).all()
            )

        if not rooms:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "code": 1,
                    "message": "No rooms found",
                    "data": "",
                },
            )

        # Process room results to include image data
        result_rooms = []

        for room in rooms:
            # Get the room's location
            location = db.query(Location).filter(Location.id == room.locationId).first()

            # First convert the room to a dict (exclude unwanted fields)
            room_dict = {
                "id": room.id,
                "name": room.name,
                "price": room.price,
                "maxPersonQty": room.maxPersonQty,
                "locationId": room.locationId,
                "create_at": room.create_at,
                "update_at": room.update_at,
                "imagePrimary": "",  # Default empty string
            }
            location_result = (
                {
                    "address": location.address,
                    "district": location.district,
                    "city": location.city,
                    "country": location.country,
                },
            )
            # Now add any additional fields that the model requires but might not be in the Room table
            if hasattr(room, "description"):
                room_dict["description"] = room.description

            if hasattr(room, "status"):
                room_dict["status"] = room.status

            # Get primary image for the room
            primary_image = (
                db.query(RoomImage)
                .filter(RoomImage.roomId == room.id, RoomImage.isPrimary == True)
                .first()
            )

            if primary_image:
                room_dict["imagePrimary"] = primary_image.url

            # Create a RoomResponse object from the dictionary
            room_data = RoomSchemas.RoomResponse(**room_dict)

            # Add to results
            result_rooms.append(
                {
                    "room": room_data.model_dump(
                        exclude={
                            "description",
                            "status",
                            "create_at",
                            "update_at",
                            "images",
                            "locationId",
                        }
                    ),
                    "location": location_result,
                }
            )

        room_searched = {
            "count": total_count,  # Total count, not just the paginated results
            "results": result_rooms,
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 0,
                "message": f"Search rooms successfully with {total_count} results",
                "data": jsonable_encoder(room_searched),
            },
        )

    except Exception as e:
        print(e)  # Print error for debugging
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 1,
                "message": f"Internal server error: {str(e)}",
                "data": "",
            },
        )


def getRoomById(roomId: int, db: Session):
    try:
        room = db.query(Room).filter(Room.id == roomId).first()
        if not room:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "code": 1,
                    "message": "Room not found",
                    "data": "",
                },
            )
        location = db.query(Location).filter(Location.id == room.locationId).first()
        result_location = {}
        if location:
            result_location = LocationSchemas.locationResponse.from_orm(
                location
            ).model_dump()
        room_dict = {
            "id": room.id,
            "name": room.name,
            "price": room.price,
            "maxPersonQty": room.maxPersonQty,
            "description": room.description,
            "status": room.status,
            "create_at": room.create_at,
            "update_at": room.update_at,
            "imagePrimary": "",  # Default empty string
            "images": [],
        }
        all_images = db.query(RoomImage).filter(RoomImage.roomId == room.id).all()
        imagePrimary = next(
            (image.url for image in all_images if image.isPrimary), None
        )
        images = [img.url for img in all_images] if all_images else []
        room_dict["imagePrimary"] = imagePrimary
        room_dict["images"] = images

        roomResponse = RoomSchemas.RoomResponse.from_orm(room_dict).model_dump()

        response = {"room": roomResponse, "location": result_location}

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 0,
                "message": "Room retrieved successfully",
                "data": jsonable_encoder(response),
            },
        )
    except Exception as e:
        print(e)  # Print error for debugging
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 1,
                "message": f"Internal server error: {str(e)}",
                "data": "",
            },
        )


def checkRoomExist(nameRoom: str, locationId: int, db: Session):
    try:
        check = (
            db.query(Room)
            .filter(and_(Room.name == nameRoom, Room.locationId == locationId))
            .first()
        )
        if check:
            return False
        return True
    except:
        return True


def createNewRoom(room: RoomSchemas.RoomCreate, db: Session):

    try:

        newRoom = Room(
            name=room.name,
            price=room.price,
            maxPersonQty=room.maxPersonQty,
            description=room.description,
            status=room.status,
            locationId=room.locationId,
        )

        db.add(newRoom)
        db.commit()
        db.refresh(newRoom)

        return newRoom.id
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": 1,
                "message": f"Internal server error: {str(e)}",
                "data": "",
            },
        )
