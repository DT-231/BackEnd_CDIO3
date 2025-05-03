# Room Booking Management System

## Mô tả dự án

Dự án **Room Booking Management System** là một hệ thống quản lý đặt phòng được xây dựng bằng **FastAPI** và **SQLAlchemy**. Hệ thống này cung cấp các API để quản lý người dùng, vai trò, phòng, địa điểm, và đặt phòng. Nó hỗ trợ các chức năng như đăng ký, đăng nhập, tìm kiếm phòng, tạo phòng mới, và quản lý thông tin đặt phòng.

## Các tính năng chính

- **Quản lý người dùng**:
  - Đăng ký tài khoản
  - Đăng nhập bằng email hoặc số điện thoại
- **Quản lý phòng**:
  - Tìm kiếm phòng theo địa điểm, giá, số lượng người, và thời gian
  - Tạo phòng mới
  - Xem chi tiết phòng
- **Quản lý đặt phòng**:
  - Đặt phòng
  - Xem danh sách đặt phòng
- **Quản lý vai trò**:
  - Xem danh sách vai trò

## Công nghệ sử dụng

- **Backend**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Authentication**: bcrypt
- **Validation**: Pydantic
- **Environment Management**: python-dotenv

## Cách chạy dự án

### 1. Cài đặt môi trường

- Tạo môi trường ảo:

```bash
  python -m venv venv
```

- Kích hoạt môi trường ảo:
  - Windows:

```bash
   .\venv\Scripts\activate
```

    - MacOS/Linux:

```bash
  source venv/bin/activate
```

- Cài các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 2. Cấu hình cơ sở dữ liệu

- Tạo file `bash.env.development` trong thư mục gốc và thêm cấu hình:

```bash
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
```

### 3. Chạy ứng dụng

- Chạy ứng dụng:

```bash
uvicorn main:app--reload
```

## Tài liệu API

### 1. **Authentication API**

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
- Response:
  - Thành công:
    ```bash
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

```bash
{
  "valueLogin": "example@example.com",
  "password": "password123"
}
```

- Response:

```bash
 { "code": 0,
  "message": "Login successful",
  "data": {
    "id": 1,
    "email": "example@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "roleId": 1 ,
          }
  }
```

### 2. Room API

#### Tìm kiếm phòng

- **Endpoint**: `/room/search`
- **Phương thức**: `GET`
- **Query Parameters**:
  `searchLocation`: Địa điểm tìm kiếm (bắt buộc).
  `person_qty`: Số lượng người (mặc định: 1).
  `check_in`: Ngày check-in (mặc định: ngày hiện tại).
  `check_out`: Ngày check-out (mặc định: ngày hiện tại + 1).
  `price_min`: Giá tối thiểu (tuỳ chọn).
  `price_max`: Giá tối đa (tuỳ chọn).
  `page`: Trang (mặc định: 1).
  `items_per_page`: Số lượng phòng mỗi trang (mặc định: 5).
  `sort_by`: Sắp xếp theo giá (price_asc hoặc price_desc).
- **Response** :
``` bash
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
  }:
```

#### Xem chi tiết phòng

- **Endpoint**: `/room/read-detail`
- **Phương thức**: `GET`
- **Query Parameters**: 
  - `roomId` : ID của phòng (bắt buộc) 
- **Response**
``` bash
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
      "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
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
``` bash
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
  "imagesRoom": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
}
```

- **Response**:
```
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
``` bash
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
