# Yêu cầu API/backend cho module Admin

Dưới đây là tổng hợp các yêu cầu về dữ liệu mà backend cần cung cấp để frontend có thể hiển thị đầy đủ giao diện Admin như mockData hiện tại. Các API nên trả về dữ liệu theo đúng cấu trúc, kiểu dữ liệu như mô tả để dễ dàng tích hợp với giao diện.

---

## 1. Thống kê tổng quan (Stat Cards)
**API:** `GET /admin/stats`
**Response:**
```json
[
  {
    "title": "Tổng bệnh nhân",
    "value": "1,248",
    "trend": "+12.0% so với tháng trước",
    "trendPositive": true,
    "icon": ""
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách các thống kê tổng quan (tổng bệnh nhân, lịch hẹn tháng này, thời gian chờ trung bình, tỉ lệ hài lòng, ...)
  - `trendPositive` xác định chiều hướng tăng/giảm

## 2. Biểu đồ lịch hẹn trong tuần
**API:** `GET /admin/weekly-appointments`
**Response:**
```json
[
  { "day": "Thứ 2", "appointments": 42 },
  ...
]
```
- **Yêu cầu:**
  - Trả về số lượng lịch hẹn theo từng ngày trong tuần

## 3. Danh sách bác sĩ hàng đầu
**API:** `GET /admin/top-doctors`
**Response:**
```json
[
  {
    "name": "Dr. Nguyễn Văn B",
    "specialty": "Hồi khoa",
    "rating": 5,
    "patients": 156
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách các bác sĩ có nhiều bệnh nhân nhất, có thể kèm theo rating

## 4. Lịch hẹn gần đây
**API:** `GET /admin/recent-appointments`
**Response:**
```json
[
  {
    "patientName": "Trần Thị A",
    "doctorName": "Dr. Nguyễn Văn B",
    "specialty": "Hồi khoa",
    "dateTime": "21/04/2026, 10:00 AM",
    "status": "confirmed"
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách các lịch hẹn gần nhất, gồm tên bệnh nhân, bác sĩ, chuyên khoa, thời gian, trạng thái

## 5. Quản lý người dùng
**API:** `GET /admin/users`
**Response:**
```json
[
  {
    "id": 1,
    "name": "Nguyễn Văn A",
    "email": "nguyenvana@example.com",
    "role": "Bác sĩ",
    "status": "active"
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách người dùng, gồm id, tên, email, vai trò, trạng thái

## 6. Quản lý bệnh viện
**API:** `GET /admin/hospitals`
**Response:**
```json
[
  {
    "id": 1,
    "name": "Bệnh viện Đa khoa Trung Ương",
    "address": "123 Đường Láng, Đống Đa, Hà Nội",
    "phone": "(024) 1234 5678"
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách bệnh viện, gồm id, tên, địa chỉ, số điện thoại

## 7. Quản lý lịch làm việc bác sĩ
**API:** `GET /admin/doctor-schedules`
**Response:**
```json
[
  {
    "doctorName": "Dr. Nguyễn Văn B",
    "specialty": "Hồi khoa",
    "schedule": {
      "Thứ 2": "08:00-12:00",
      "Thứ 3": "14:00-17:00",
      ...
    }
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách lịch làm việc của từng bác sĩ theo từng ngày trong tuần

## 8. Quản lý thanh toán
**API:** `GET /admin/payments`
**Response:**
```json
[
  {
    "id": "#INV001",
    "userName": "Nguyễn Văn A",
    "amount": "1,500,000đ",
    "method": "Chuyển khoản",
    "status": "success",
    "date": "20/04/2026"
  },
  ...
]
```
- **Yêu cầu:**
  - Trả về danh sách giao dịch, gồm mã giao dịch, tên người dùng, số tiền, phương thức, trạng thái, ngày
  - Thêm API trả về thống kê tổng doanh thu, giao dịch thành công, đang xử lý, thất bại (có thể gộp vào `/admin/stats` hoặc tách riêng)

## 9. Cài đặt hệ thống
**API:** `GET /admin/settings`
**Response:**
```json
{
  "systemName": "MediCare System",
  "supportEmail": "support@medicare.com",
  "phone": "1900 1234",
  "address": "Hà Nội, Việt Nam",
  "timezone": "Asia/Ho_Chi_Minh",
  "dateFormat": "DD/MM/YYYY",
  "notifications": {
    "email": true,
    "sms": false,
    "push": true
  },
  "security": {
    "twoFactor": false,
    "sessionTimeout": true
  }
}
```
- **Yêu cầu:**
  - Trả về thông tin cấu hình hệ thống, thông báo, bảo mật

---

**Lưu ý:**
- Các API nên hỗ trợ phân trang, lọc, tìm kiếm nếu dữ liệu lớn
- Các trường status nên có enum rõ ràng (active, pending, completed, ...)
- Định dạng ngày/thời gian nên nhất quán
- Các API thêm/sửa/xóa (POST/PUT/DELETE) không liệt kê ở đây, chỉ tập trung vào dữ liệu để hiển thị
