from fastapi import APIRouter

from app.controllers.AuthController import handle_Login_User, handle_Register_User
from app.schemas.BaseResponseSchemas import SuccessResponse
from app.utils.errorResponseDoc import error_response
from app.schemas.UserSchemas import UserSchemas

AuthRouter = APIRouter(prefix="/auth", tags=["auth"])

AuthRouter.add_api_route(
    "/register",
    endpoint=handle_Register_User,
    methods=["POST"],
    response_model=SuccessResponse,
    tags=["auth"],
    responses=error_response(status=[400, 422, 500]),
)


AuthRouter.add_api_route(
    "/login",
    endpoint=handle_Login_User,
    methods=["POST"],
    response_model=SuccessResponse[UserSchemas.UserResponse],
    tags=["auth"],
    responses=error_response(status=[400, 422, 500]),
)
