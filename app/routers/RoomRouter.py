from fastapi import APIRouter

from app.controllers.RoomController import (
    HandleCreateRoom,
    HandleSearchRooms,
    HandleReadRoomDetail,
    # HandleGetALL
)
from app.schemas import RoomSchemas
from app.schemas.BaseResponseSchemas import SuccessResponse
from app.utils.errorResponseDoc import error_response


RoomRouter = APIRouter(prefix="/room", tags=["room"])



RoomRouter.add_api_route(
    "/search",
    endpoint=HandleSearchRooms,
    methods=["GET"],
    response_model=SuccessResponse[RoomSchemas.RoomResponse],
    tags=["room"],
    responses=error_response(status=[400, 422, 500]),
)

# RoomRouter.add_api_route(
#     "/get-all",
#     endpoint=HandleGetALL,
#     methods=["GET"],
#     response_model=SuccessResponse[RoomSchemas.RoomResponse],
#     tags=["room"],
#     responses=error_response(status=[400, 422, 500]),
# )

RoomRouter.add_api_route(
    "/read-detail",
    endpoint=HandleReadRoomDetail,
    methods=["GET"],
    response_model=SuccessResponse[RoomSchemas.RoomResponse],
    tags=["room"],
    responses=error_response(status=[400, 422, 500]),
)

RoomRouter.add_api_route(
    "/create",
    endpoint=HandleCreateRoom,
    methods=["POST"],
    response_model=SuccessResponse[RoomSchemas.RoomResponse],
    tags=["room"],
    responses=error_response(status=[400, 422, 500]),
)
