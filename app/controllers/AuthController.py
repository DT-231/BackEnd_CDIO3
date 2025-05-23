from typing import Optional
from fastapi import Depends, Request, Response, status
from fastapi.params import Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.databases import get_db

from app.schemas.UserSchemas import UserSchemas
from app.services.AuthService import (
    createNewUser,
    loginUser,
    validateEmail,
    validatePhoneNumber,
)


async def handle_Register_User(
    request: Request,
    email: Optional[str] = Body(None),
    password: str = Body(...),
    phoneNumber: Optional[str] = Body(None),
    firstName: str = Body(...),
    lastName: str = Body(...),
    roleId: Optional[int] = Body(1),
    db: Session = Depends(get_db),
):

    try:
        if (
            not email
            and not phoneNumber
            or not password
            or not firstName
            or not lastName
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "code": 1,
                    "message": "Missing required fields",
                    "data": "",
                },
            )

        validEmail = validateEmail(email)
        validPhoneNumber = validatePhoneNumber(phoneNumber)

        if not validEmail and not validPhoneNumber:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "code": 1,
                    "message": "Invalid email or phone number format",
                    "data": "",
                },
            )
        if len(password) < 8:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "code": 1,
                    "message": "password ít nhất phải có 8 ký tự",
                    "data": "",
                },
            )
        user = UserSchemas.UserCreate(
            email=email,
            phoneNumber=phoneNumber,
            firstName=firstName,
            lastName=lastName,
            password=password,
            roleId=roleId,
        )

        new_user = createNewUser(db=db, user=user)

        return new_user

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": -1,
                "message": "Internal Server Error",
                "data": "",
            },
        )


async def handle_Login_User(
    request: Request,
    valueLogin: str = Body(None),
    password: str = Body(None),
    db: Session = Depends(get_db),
):
    try:
        if not valueLogin or not password:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "code": 1,
                    "message": "Missing required fields",
                    "data": "",
                },
            )
        # Check if the username already exists
        validEmail = validateEmail(valueLogin)

        validPhoneNumber = validatePhoneNumber(valueLogin)
        if not validEmail and not validPhoneNumber:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "code": 1,
                    "message": "Invalid email or phone number format",
                    "data": "",
                },
            )

        user = None
        # Check if valueLogin is a phone number or username
        if valueLogin.isdigit():
            user = UserSchemas.UserBase(
                phoneNumber=valueLogin,
                password=password,
            )
        else:
            user = UserSchemas.UserBase(
                email=valueLogin,
                password=password,
            )

        respone = loginUser(db=db, user=user)
        return respone

    except Exception as e:
        print(f"Error checking email: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": -1,
                "message": "Internal Server Error",
                "data": "",
            },
        )
