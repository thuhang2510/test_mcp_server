# Changelog - Thêm Thông Tin Cơ Bản

## Phiên bản mới - Ngày 19/01/2025

### ✨ Tính năng mới

Đã thêm thành công **4 trường thông tin cơ bản** cho mỗi người trong hệ thống:

#### 📧 Email
- Lưu trữ địa chỉ email của từng người  
- VD: `hang.dam@email.com`, `minh.tran@company.vn`

#### 📱 Số điện thoại  
- Lưu trữ số điện thoại liên lạc
- VD: `0123456789`, `0987654321`

#### 🏠 Địa chỉ nhà
- Địa chỉ cư trú đầy đủ
- VD: `123 Đường Lê Lợi, Quận 1, TP.HCM`

#### 👔 Nghề nghiệp
- Công việc hiện tại 
- VD: `Sinh viên`, `Kỹ sư phần mềm`

### 🔧 Cập nhật kỹ thuật

#### Dữ liệu mẫu
- **Hang**: Sinh viên 18 tuổi, email hang.dam@email.com, ở Quận 1 TP.HCM
- **Minh**: Kỹ sư phần mềm 22 tuổi, email minh.tran@company.vn, ở Quận 3 TP.HCM

#### API Tools mới
Thêm 5 tools mới để truy xuất thông tin:

1. `get_contact_info(name)` - Lấy tất cả thông tin liên lạc (email + phone + address)
2. `get_email(name)` - Lấy địa chỉ email
3. `get_phone(name)` - Lấy số điện thoại  
4. `get_address(name)` - Lấy địa chỉ nhà
5. `get_occupation(name)` - Lấy nghề nghiệp

#### Cập nhật tools có sẵn
- `get_profile(name)` - Bây giờ bao gồm 4 trường thông tin mới
- `search_people(query)` - Có thể tìm kiếm theo email, phone, address, occupation
- `list_people(include_profiles=True)` - Profile đầy đủ bao gồm thông tin liên lạc

### 🔍 Tính năng tìm kiếm nâng cao

Bây giờ có thể tìm kiếm theo:
- Tên miền email: `search_people("gmail")`  
- Số điện thoại: `search_people("0123")`
- Khu vực: `search_people("Quận 1")`
- Nghề nghiệp: `search_people("kỹ sư")`

### ✅ Testing

- ✓ Tất cả dữ liệu mới đã được thêm thành công
- ✓ Format email, phone, address hợp lệ  
- ✓ Tính năng tìm kiếm hoạt động với trường mới
- ✓ Backward compatibility với code cũ được đảm bảo
- ✓ Syntax Python hợp lệ

### 📋 Sử dụng

```python
# Lấy thông tin liên lạc đầy đủ
get_contact_info("Hang")
# => {"person": "Hang", "email": "hang.dam@email.com", "phone": "0123456789", "address": "123 Đường Lê Lợi, Quận 1, TP.HCM"}

# Lấy nghề nghiệp  
get_occupation("Minh")
# => {"person": "Minh", "occupation": "Kỹ sư phần mềm"}

# Tìm kiếm theo nghề nghiệp
search_people("sinh viên")
# => Trả về danh sách people có nghề nghiệp chứa "sinh viên"

# Profile đầy đủ
get_profile("Hang")
# => Bao gồm tất cả thông tin cũ + email, phone, address, occupation mới
```

Tất cả tính năng đã được implement thành công và sẵn sàng sử dụng! 🎉