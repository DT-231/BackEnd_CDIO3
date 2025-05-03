from fastapi import APIRouter
from app.controllers.RoleController import HandleReadRoles
from app.schemas import RoleSchemas
from app.schemas.BaseResponseSchemas import SuccessResponse
from app.utils.errorResponseDoc import error_response

RoleRouter = APIRouter(prefix="/role", tags=["role"])

RoleRouter.add_api_route(
    "/read",
    endpoint=HandleReadRoles,
    methods=["GET"],
    response_model=SuccessResponse[RoleSchemas.RoleResponse],
    tags=["role"],
    responses=error_response(status=[400, 422, 500]),
    response_description="Get all roles",
)
