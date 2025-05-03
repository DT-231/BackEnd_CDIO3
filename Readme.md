# Room Booking Management System

## 📝 Tổng quan

Dự án **Room Booking Management System** là một hệ thống quản lý đặt phòng được xây dựng bằng **FastAPI** và **SQLAlchemy**. Hệ thống cung cấp các API để quản lý người dùng, vai trò, phòng, địa điểm và đặt phòng. Nó hỗ trợ các chức năng như đăng ký, đăng nhập, tìm kiếm phòng, tạo phòng mới và quản lý thông tin đặt phòng.

## ✨ Tính năng chính

### 👤 Quản lý người dùng
- Đăng ký tài khoản mới
- Đăng nhập bằng email hoặc số điện thoại
- Quản lý thông tin cá nhân

### 🏨 Quản lý phòng
- Tìm kiếm phòng theo địa điểm, giá, số lượng người và thời gian
- Tạo và cập nhật thông tin phòng
- Xem chi tiết phòng với hình ảnh

### 📅 Quản lý đặt phòng
- Đặt phòng với các thông tin chi tiết
- Xem lịch sử và danh sách đặt phòng

### 👮 Quản lý vai trò (Role)
- Phân quyền người dùng
- Xem danh sách vai trò trong hệ thống

## 🛠️ Công nghệ sử dụng

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - Framework API hiệu suất cao
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Thư viện SQL Toolkit
- **Database**: MySQL - Hệ quản trị cơ sở dữ liệu quan hệ
- **Authentication**: bcrypt - Thư viện mã hóa mật khẩu
- **Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Thư viện xác thực dữ liệu
- **Environment Management**: python-dotenv - Quản lý biến môi trường

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8+
- MySQL

### 2. Cài đặt môi trường

#### Sao chép mã nguồn
```bash
git clone <repository-url>
cd room-booking-system
```

#### Tạo và kích hoạt môi trường ảo
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo (Windows)
.\venv\Scripts\activate

# Kích hoạt môi trường ảo (MacOS/Linux)
source venv/bin/activate
```

#### Cài đặt các thư viện
```bash
pip install -r requirements.txt
```

### 3. Cấu hình cơ sở dữ liệu

Tạo file `.env.development` trong thư mục gốc và thêm cấu hình:

```
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=your_secret_key_here
```

### 4. Khởi tạo cơ sở dữ liệu
```bash
# Chạy migration (nếu có)
alembic upgrade head
```

### 5. Chạy ứng dụng
```bash
uvicorn main:app --reload
```

Ứng dụng sẽ chạy tại địa chỉ: `http://localhost:8000`

## 📚 Tài liệu API

Sau khi khởi động ứng dụng, bạn có thể truy cập tài liệu API tự động tại:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 1. Authentication API

#### Đăng ký tài khoản

- **Endpoint**: `/auth/register`
- **Phương thức**: `POST`
- **Request Body**:
  ```json
  {
    "email": "example@example.com",
    "password": "password123",
    "phoneNumber": "0123456789",
    "firstName": "John",
    "lastName": "Doe",
    "roleId": 1
  }
  ```
- **Response**:
  ```json
  {
    "code": 0,
    "message": "User created successfully",
    "data": ""
  }
  ```

#### Đăng nhập

- **Endpoint**: `/auth/login`
- **Phương thức**: `POST`
- **Request Body**:
  ```json
  {
    "valueLogin": "example@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "code": 0,
    "message": "Login successful",
    "data": {
      "id": 1,
      "email": "example@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "roleId": 1
    }
  }
  ```

### 2. Room API

#### Tìm kiếm phòng

- **Endpoint**: `/room/search`
- **Phương thức**: `GET`
- **Query Parameters**:
  - `searchLocation`: Địa điểm tìm kiếm (bắt buộc)
  - `person_qty`: Số lượng người (mặc định: 1)
  - `check_in`: Ngày check-in (mặc định: ngày hiện tại)
  - `check_out`: Ngày check-out (mặc định: ngày hiện tại + 1)
  - `price_min`: Giá tối thiểu (tuỳ chọn)
  - `price_max`: Giá tối đa (tuỳ chọn)
  - `page`: Trang (mặc định: 1)
  - `items_per_page`: Số lượng phòng mỗi trang (mặc định: 5)
  - `sort_by`: Sắp xếp theo giá (price_asc hoặc price_desc)
- **Response**:
  ```json
  {
    "code": 0,
    "message": "Search rooms successfully with 10 results",
    "data": {
      "count": 10,
      "results": [
        {
          "room": {
            "id": 1,
            "name": "Deluxe Room",
            "price": 100.0,
            "maxPersonQty": 2,
            "imagePrimary": "https://example.com/image.jpg"
          },
          "location": {
            "address": "123 Street",
            "city": "Hanoi",
            "country": "Vietnam"
          }
        }
      ]
    }
  }
  ```

#### Xem chi tiết phòng

- **Endpoint**: `/room/read-detail`
- **Phương thức**: `GET`
- **Query Parameters**: 
  - `roomId`: ID của phòng (bắt buộc) 
- **Response**:
  ```json
  {
    "code": 0,
    "message": "Room retrieved successfully",
    "data": {
      "room": {
        "id": 1,
        "name": "Deluxe Room",
        "price": 100.0,
        "maxPersonQty": 2,
        "description": "A luxurious room",
        "status": "available",
        "imagePrimary": "https://example.com/image.jpg",
        "images": [
          "https://example.com/image1.jpg", 
          "https://example.com/image2.jpg"
        ]
      },
      "location": {
        "address": "123 Street",
        "city": "Hanoi",
        "country": "Vietnam"
      }
    }
  }
  ```

#### Tạo phòng mới
- **Endpoint**: `/room/create`
- **Phương thức**: `POST`
- **Request Body**:
  ```json
  {
    "name": "Deluxe Room",
    "price": 100.0,
    "maxPersonQty": 2,
    "description": "A luxurious room",
    "status": "available",
    "address": "123 Street",
    "district": "District 1",
    "city": "Hanoi",
    "country": "Vietnam",
    "description_location": "Near the city center",
    "imagesRoom": [
      "https://example.com/image1.jpg", 
      "https://example.com/image2.jpg"
    ]
  }
  ```

- **Response**:
  ```json
  {
    "code": 0,
    "message": "Tạo phòng thành công",
    "data": ""
  }
  ```

### 3. Role API 

#### Lấy danh sách role
- **Endpoint**: `/role/read`
- **Phương thức**: `GET`
- **Response**:
  ```json
  {
    "code": 0,
    "message": "Roles retrieved successfully",
    "data": [
      {
        "id": 1,
        "name": "Admin",
        "description": "Administrator role"
      },
      {
        "id": 2,
        "name": "User",
        "description": "Regular user role"
      }
    ]
  }
  ```

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request để đóng góp vào dự án.

## 📄 Giấy phép

Dự án này được phát hành dưới giấy phép [MIT](LICENSE).