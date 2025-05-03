from fastapi.encoders import jsonable_encoder
import pydantic
import re
import bcrypt
from fastapi.responses import JSONResponse
from fastapi import status
from phonenumbers import is_valid_number, parse
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserSchemas


def validateEmail(value) -> bool:
    try:
        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value)
    except:
        valid = None
    return valid


def validatePhoneNumber(value) -> str:
    valid = None
    try:
        if value.startswith("0"):
            value = "+84" + value[1:]
        valid = is_valid_number(parse(value))
    except Exception as e:
        print(e)
    return valid


def hash_password(password: str) -> str:

    # converting password to array of bytes
    bytes = password.encode("utf-8")

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    return hash.decode("utf-8")


def check_password(password_input: str, hashed_password: str) -> bool:
    # Convert the input password to bytes
    try:
        # Convert the input password to bytes
        password_bytes = password_input.encode("utf-8")

        # Compare the input password with the hashed password
        result = bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
        print(f"Password check result: {result}")
        return result
    except Exception as e:
        print(f"Password check error: {str(e)}")
        return False


def check_phone_number_exists(db: Session, phoneNumber: str) -> bool:

    if not phoneNumber:
        return True
    try:
        checkPhoneNumber = (
            db.query(User).filter(User.phoneNumber == phoneNumber).first()
        )
        if checkPhoneNumber is None:
            return True
        return False

    except Exception as e:
        print(f"Error checking phone number: {str(e)}")
        return False


def check_email_exists(db: Session, email: str) -> bool:

    if not email:
        return True
    try:
        checkUser = db.query(User).filter(User.email == email).first()
        if checkUser is None:
            return True
        return False

    except Exception as e:
        print(f"Error checking email: {str(e)}")
        return False


def createNewUser(
    db: Session, user: UserSchemas.UserCreate
) -> UserSchemas.UserResponse:

    try:
        # Check if the username already exists
        checkUser = check_email_exists(db, user.email)
        if checkUser is False:

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 1,
                    "message": "User already exists",
                    "data": "",
                },
            )

        # Check if the phone number already exists
        checkPhoneNumber = check_phone_number_exists(db, user.phoneNumber)
        if checkPhoneNumber is False:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 1,
                    "message": "Phone number already exists",
                    "data": "",
                },
            )

        hashed_password = hash_password(user.password)
        # Create a new user instance
        new_user = User(
            email=user.email,
            password=hashed_password,
            firstName=user.firstName,
            lastName=user.lastName,
            roleId=user.roleId,
            phoneNumber=user.phoneNumber,
        )
        # Add the new user to the database session
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"code": 0, "message": "User created successfully", "data": ""},
        )

    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": -2,
                "message": "Something wrongs in service...",
                "data": "",
            },
        )


def loginUser(db: Session, user: UserSchemas.UserBase) -> UserSchemas.UserResponse:
    try:
        # Check if the username already exists
        checkUser = (
            db.query(User)
            .filter(
                or_(
                    and_(User.email == user.email, user.email is not None),
                    and_(
                        User.phoneNumber == user.phoneNumber,
                        user.phoneNumber is not None,
                    ),
                )
            )
            .first()
        )

        if checkUser is None:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 1,
                    "message": "User not found",
                    "data": "",
                },
            )
        # Check if the password is correct
        if not check_password(user.password, checkUser.password):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 1,
                    "message": "Incorrect password",
                    "data": "",
                },
            )
        # response = [
        # ),"role":checkUser.role.name]
        print(f"User found: {checkUser}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 0,
                "message": "Login successful",
                "data": jsonable_encoder(
                    UserSchemas.UserResponse.from_orm(checkUser).model_dump(
                        exclude={"password"}
                    )
                ),
            },
        )

    except Exception as e:
        print(f"Error creating user: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": -2,
                "message": "Something wrongs in service...",
                "data": "",
            },
        )
