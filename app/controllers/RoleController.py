from fastapi import Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.databases import get_db
from app.models import Role
from app.schemas import RoleSchemas
from app.services.RoleService import getAllRoles


async def HandleReadRoles(request: Request, db: Session = Depends(get_db)):
    try:
        response = getAllRoles(db)

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
