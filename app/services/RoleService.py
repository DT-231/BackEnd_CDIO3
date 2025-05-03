from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.models import Role
from sqlalchemy.orm import Session

from app.schemas import RoleSchemas


def getAllRoles(db: Session):
    try:
        role_raw = db.query(Role).all()
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
