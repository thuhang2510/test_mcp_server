# Demo Tính Năng: Thêm Người Mới

## Tổng quan
Tool `add_person` cho phép thêm người mới vào hệ thống quản lý thông tin người dùng với validation đầy đủ.

## Cách sử dụng cơ bản

### 1. Thêm người với thông tin đầy đủ
```python
add_person(
    name="Lan Nguyen",
    age=25,
    birthday="15/8",
    email="lan.nguyen@example.com",
    phone="0901234567",
    address="789 Đường Võ Văn Tần, Quận 10, TP.HCM",
    occupation="Thiết kế đồ họa",
    work_experience_years=3,
    father="Nguyen VT",
    mother="Tran TH",
    siblings="Nguyen DL",
    hobby="Vẽ tranh",
    quote="Sáng tạo không có giới hạn",
    favorite_color="Hồng"
)
```

**Kết quả:**
```json
{
  "success": true,
  "message": "Đã thêm người mới 'Lan Nguyen' thành công vào hệ thống",
  "person_count": 3,
  "profile": {
    "age": 25,
    "birthday": "15/8",
    "work_experience_years": 3,
    "email": "lan.nguyen@example.com",
    "phone": "0901234567",
    "address": "789 Đường Võ Văn Tần, Quận 10, TP.HCM",
    "occupation": "Thiết kế đồ họa",
    "family": {
      "father": "Nguyen VT",
      "mother": "Tran TH",
      "siblings": "Nguyen DL"
    },
    "hobby": "Vẽ tranh",
    "quote": "Sáng tạo không có giới hạn",
    "favorite_color": "Hồng"
  }
}
```

### 2. Thêm người với thông tin tối thiểu
```python
add_person(
    name="An Vo",
    age=30,
    birthday="22/12",
    email="an.vo@company.com",
    phone="0912345678"
)
```

**Kết quả:**
```json
{
  "success": true,
  "message": "Đã thêm người mới 'An Vo' thành công vào hệ thống",
  "person_count": 4,
  "profile": {
    "age": 30,
    "birthday": "22/12",
    "work_experience_years": 0,
    "email": "an.vo@company.com",
    "phone": "0912345678"
  }
}
```

## Xử lý lỗi

### 1. Tên trùng lặp
```python
add_person(
    name="Hang",  # Tên đã tồn tại
    age=20,
    birthday="1/1",
    email="test@example.com",
    phone="0123456789"
)
```

**Kết quả:**
```json
{
  "success": false,
  "error": "Người có tên 'Hang' đã tồn tại trong hệ thống"
}
```

### 2. Email không hợp lệ
```python
add_person(
    name="Test Person",
    age=25,
    birthday="15/8",
    email="invalid-email",  # Email sai format
    phone="0901234567"
)
```

**Kết quả:**
```json
{
  "success": false,
  "error": "Email không đúng định dạng"
}
```

### 3. Ngày sinh sai định dạng
```python
add_person(
    name="Test Person 2",
    age=25,
    birthday="2023-08-15",  # Format sai
    email="test2@example.com",
    phone="0901234567"
)
```

**Kết quả:**
```json
{
  "success": false,
  "error": "Ngày sinh phải theo định dạng dd/mm (ví dụ: 25/10)"
}
```

## Validation Rules

| Trường | Quy tắc | Ví dụ hợp lệ |
|--------|---------|--------------|
| `name` | Không được trống, không trùng lặp | "Lan Nguyen" |
| `age` | Số nguyên từ 0-150 | 25 |
| `birthday` | Định dạng dd/mm hoặc d/m | "15/8", "5/12" |
| `email` | Định dạng email chuẩn | "user@domain.com" |
| `phone` | 8-15 chữ số | "0901234567" |

## Tích hợp với các tool khác

Sau khi thêm người mới thành công, bạn có thể sử dụng các tool khác:

- `get_info("Lan Nguyen")` - Lấy thông tin chi tiết
- `calculate_age("Lan Nguyen")` - Tính tuổi chính xác
- `get_zodiac("Lan Nguyen")` - Xem cung hoàng đạo
- `calculate_compatibility("Lan Nguyen", "Minh")` - Tính độ hợp nhau

## Lưu ý quan trọng

1. **Tên không phân biệt hoa thường**: "Lan Nguyen" và "lan nguyen" được coi là trùng nhau
2. **Thông tin gia đình linh hoạt**: Có thể thêm father, mother, siblings tùy ý
3. **work_experience_years**: Mặc định là 0 nếu không cung cấp
4. **Dữ liệu lưu trong bộ nhớ**: Khởi động lại server sẽ mất dữ liệu đã thêm