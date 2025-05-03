from sqlalchemy import Column, Integer
from app.databases import Base


class BaseModel(Base):
    __abstract__ = True  # Đánh dấu đây là lớp trừu tượng, không tạo bảng riêng
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
