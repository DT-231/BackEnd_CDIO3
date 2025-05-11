from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

#
app = FastAPI()

from app.databases import engine, Base, get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.models import Room, Location, User, Role, RoomImage

Base.metadata.create_all(bind=engine)


def check_connection_mySql():
    try:
        db: Session = next(get_db())  # Lấy session đầu tiên từ get_db()
        db.execute(text("SELECT 1"))  # Chạy câu lệnh đơn giản để kiểm tra
    except Exception as e:
        print("Lỗi kết nối DB:", e)


check_connection_mySql()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lắng nghe tất cả domain
    allow_credentials=True,
    allow_methods=[
        "*"
    ],  #  ["*"] lắng nghe tất cả method / ["POST", "GET", "OPTIONS"] nếu muốn giới hạn
    allow_headers=["*"],
)


from app.routers import AuthRouter

app.include_router(AuthRouter)

from app.routers import RoleRouter

app.include_router(RoleRouter)

from app.routers import RoomRouter

app.include_router(RoomRouter)


