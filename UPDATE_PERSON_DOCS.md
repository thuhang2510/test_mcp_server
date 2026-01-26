# Tính năng Update Person

## Mô tả
Tool `update_person` cho phép cập nhật thông tin cá nhân của những người đã có trong hệ thống.

## Cú pháp
```
update_person(name, field, new_value)
```

### Tham số:
- **name** (str): Tên người cần cập nhật
- **field** (str): Trường cần cập nhật  
- **new_value** (str): Giá trị mới

### Các trường hỗ trợ cập nhật:
- `email` - Địa chỉ email
- `phone` - Số điện thoại
- `address` - Địa chỉ nhà
- `occupation` - Nghề nghiệp
- `hobby` - Sở thích
- `quote` - Câu nói yêu thích
- `favorite_color` - Màu sắc yêu thích

### Aliases (tên gọi khác) được hỗ trợ:
- Email: `email`, `mail`, `e-mail`
- Phone: `phone`, `telephone`, `tel`, `sdt`, `số điện thoại`
- Address: `address`, `địa chỉ`, `dia_chi`
- Occupation: `occupation`, `job`, `work`, `nghề nghiệp`
- Hobby: `hobby`, `sở thích`, `so_thich`
- Quote: `quote`, `câu nói`, `cau_noi`
- Favorite Color: `favorite_color`, `màu yêu thích`, `color`

## Ví dụ sử dụng

### Cập nhật email:
```python
update_person("Hang", "email", "hang.new@gmail.com")
```

### Cập nhật số điện thoại (tiếng Việt):
```python
update_person("Minh", "số điện thoại", "0901234567")
```

### Cập nhật địa chỉ:
```python
update_person("Hang", "address", "789 Đường Võ Văn Tần, Quận 3, TP.HCM")
```

### Cập nhật nghề nghiệp:
```python
update_person("Minh", "occupation", "Senior Software Engineer")
```

### Cập nhật sở thích:
```python
update_person("Hang", "hobby", "Vẽ tranh và chụp ảnh nghệ thuật")
```

## Response Format

### Khi thành công:
```json
{
    "success": true,
    "message": "Đã cập nhật email của Hang",
    "person": "Hang",
    "field": "email", 
    "old_value": "hang.dam@email.com",
    "new_value": "hang.new@gmail.com",
    "updated_profile": { ... }
}
```

### Khi có lỗi:
```json
{
    "success": false,
    "message": "Không tìm thấy người có tên 'Unknown' trong hệ thống",
    "available_people": ["Hang", "Minh"]
}
```

## Validation

### Email validation:
- Phải chứa ký tự `@`
- Phải có dấu `.` sau `@`

### Phone validation:
- Phải chứa ít nhất một chữ số

### General validation:
- Giá trị không được rỗng
- Trường phải thuộc danh sách hỗ trợ
- Người được cập nhật phải tồn tại trong hệ thống

## Lưu ý
- Các trường `age`, `birthday`, `family` không thể cập nhật qua tool này
- Tên người không phân biệt hoa thường
- Tool hỗ trợ tên trường bằng tiếng Việt và tiếng Anh
- Thay đổi sẽ được lưu ngay lập tức vào hệ thống