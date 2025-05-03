FROM python:3.9-slim

WORKDIR /app

# Cài đặt đầy đủ các dependencies cần thiết cho mysqlclient và các thư viện khác
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Thử cài đặt với verbose để xem lỗi chi tiết
RUN pip install --no-cache-dir --verbose pip wheel setuptools
# Cài đặt mysqlclient riêng trước
RUN pip install --no-cache-dir --verbose mysqlclient
# Sau đó cài đặt các thư viện còn lại
RUN pip install --no-cache-dir --verbose -r requirements.txt

COPY . .

# Mặc định PORT là 8080 nhưng có thể được ghi đè bởi Railway
ENV PORT=8080

# Sử dụng biến môi trường PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}