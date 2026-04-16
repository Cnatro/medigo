# MediGo - Flask Clean Architecture + CQRS

Đặt lịch khám, khám bệnh

# Cấu trúc dự án

```
medigo/
│
├── app/
│   ├── api/
│   │   └── app.py
│   │
│   ├── config.py
│   ├── dependencies.py
│   │
│   ├── core/
│   │   ├── entities/
│   │   ├── repositories/
│   │   ├── services/
│   │
│   ├── infrastructure/
│   │   ├── db.py
│   │   ├── models/
│   │   ├── repositories/
│   │
│   ├── interfaces/
│   │   ├── controllers/
│   │   ├── mappers/
│   │   ├── routes/
│   │   └── shared/
│   │       └── utils/
│   │         
│
├── manage.py
├── run.py
├── requirements.txt
│
├── migrations/
│  
└── tests/
```

---

# Tổng quan kiến trúc

Dự án MediGo sử dụng:

- Flask (framework)
- Clean Architecture (tách business và database)
- CQRS (Command Query Responsibility Segregation)

Mục tiêu:

- Tách business logic khỏi DB
- Code dễ đọc, không rối
- Dễ mở rộng và test

---

# Phân chia layer

## 1. Core (Business - KHÔNG DB)

Chứa toàn bộ logic nghiệp vụ:

- entities: model thuần (không phụ thuộc framework)
- services: xử lý business logic
- repositories: interface (không chứa SQLAlchemy)

Đây là nơi quan trọng nhất của hệ thống

---

## 2. Infrastructure (Database)

Chứa:

- SQLAlchemy models
- Repository implementation
- DB connection

Chỉ layer này được phép làm việc với database

---

## 3. Interfaces (HTTP layer)

Chứa:

- Controller (xử lý request)
- Routes (mapping URL)

Không chứa business logic

---

# CQRS trong MediGo

CQRS = Command Query Responsibility Segregation

Tách rõ 2 loại logic:

## Command (WRITE)

- Create
- Update
- Delete
- Có business rule

---

## Query (READ)

- Chỉ đọc dữ liệu
- Không chứa business logic phức tạp

---

# Cách áp dụng CQRS trong structure này

Không tách folder riêng Áp dụng trực tiếp trong service

---

## Ví dụ: booking\_service.py

```python
class BookingService:

    def __init__(self, booking_repo, schedule_repo):
        self.booking_repo = booking_repo
        self.schedule_repo = schedule_repo

    #  COMMAND
    def create_booking(self, data):
        if not self.schedule_repo.is_available(data["schedule_id"]):
            raise Exception("Slot not available")

        return self.booking_repo.create(data)

    #  QUERY
    def get_bookings(self, user_id):
        return self.booking_repo.find_by_user(user_id)
```

---

# Flow hoạt động

## WRITE FLOW

```
HTTP Request
   ↓
Route
   ↓
Controller
   ↓
Service (Command)
   ↓
Repository
   ↓
Database
```

---

## READ FLOW

```
HTTP Request
   ↓
Route
   ↓
Controller
   ↓
Service (Query)
   ↓
Repository
   ↓
Database
```

---

# Nguyên tắc quan trọng

## 1. Core không phụ thuộc DB

- Không import SQLAlchemy
- Không import Flask

---

## 2. Repository là interface

- Định nghĩa trong core
- Implement ở infrastructure

---

## 3. Service chứa business logic

- Không gọi trực tiếp DB
- Chỉ gọi repository

---

## 4. Controller không chứa business

- Chỉ nhận request và gọi service

---

# Migration (database)

Khởi tạo migration:
```
flask db init
```

Tạo migration mới (sau khi thay đổi models):
```
flask db migrate -m "message"
```
hoặc (nếu dùng manage.py):
```
flask --app manage.py db migrate -m "message"
```

Nâng cấp database:
```
flask db upgrade
```
hoặc:
```
flask --app manage.py db upgrade
```
