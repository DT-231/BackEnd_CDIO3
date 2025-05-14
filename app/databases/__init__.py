import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()

# load_dotenv(dotenv_path=".env.development")

# #  lấy database url từ biến môi trườngtrường
# Database_url = os.getenv("DATABASE_URL")

# print("database tu env:", Database_url)
# Kết nối đến MySQL

engine = create_engine(
    "mysql+pymysql://yhgsqecv_qlks_cua_den:group_123@dinlaan.com:3306/yhgsqecv_qlks_cua_den",
    echo=True,
    pool_pre_ping=True,
)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base để tạo model
Base = declarative_base()


# Dependency để lấy database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print("Lỗi kết nối DB:", e)
    finally:
        db.close()
