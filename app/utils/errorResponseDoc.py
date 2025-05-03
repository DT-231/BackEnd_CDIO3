
from app.schemas.BaseResponseSchemas import ErrorResponse

baseErrorResponse = {
    400: {
        "model": ErrorResponse,
        "description": "Invalid input",
        "content": {
            "application/json": {
                "example": {
                    "code": 1,
                    "message": "Invalid email or phone number format",
                    "data": "",
                }
            }
        },
    },
    500: {
        "model": ErrorResponse,
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "code": -1,
                    "message": "Internal Server Error",
                    "data": "",
                }
            }
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {"code": 1, "message": "Validation error", "data": ""}
            }
        },
    },
}


def error_response(
    status: list[int] = [400, 500], message: dict[int, str] = {}
) -> dict:
    response = {}
    for code in status:
        base = baseErrorResponse.get(code)
        if base:
            # Ghi đè message nếu có tuỳ chỉnh
            if code in message:
                base = {
                    **base,
                    "content": {
                        "application/json": {
                            "example": {
                                **base["content"]["application/json"]["example"],
                                "message": message[code],
                            }
                        }
                    },
                }
            response[code] = base
    return response
