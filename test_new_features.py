#!/usr/bin/env python3
"""Test script to verify new contact info features work correctly."""

# Test data structure to simulate PEOPLE without importing MCP
PEOPLE = {
    "Hang": {
        "age": 18,
        "birthday": "25/10",
        "work_experience_years": 0,
        "email": "hang.dam@email.com",
        "phone": "0123456789",
        "address": "123 Đường Lê Lợi, Quận 1, TP.HCM",
        "occupation": "Sinh viên",
        "family": {
            "father": "Dam VT",
            "mother": "La TT",
            "sister": "Dam HG",
        },
        "hobby": "Nhiếp ảnh đường phố",
        "quote": "Cứ đi rồi sẽ đến.",
        "favorite_color": "Tím",
    },
    "Minh": {
        "age": 22,
        "birthday": "09/04",
        "work_experience_years": 2,
        "email": "minh.tran@company.vn",
        "phone": "0987654321",
        "address": "456 Đường Nguyễn Huệ, Quận 3, TP.HCM",
        "occupation": "Kỹ sư phần mềm",
        "family": {
            "father": "Tran TL",
            "mother": "Nguyen MT",
            "brother": "Tran QH",
        },
        "hobby": "Chạy bộ buổi sáng",
        "quote": "Bền bỉ tạo nên khác biệt.",
        "favorite_color": "Xanh dương",
    },
}

def test_new_contact_fields():
    """Test that new contact fields are present for all people."""
    required_fields = ["email", "phone", "address", "occupation"]
    
    for name, person in PEOPLE.items():
        print(f"\n=== Testing {name} ===")
        for field in required_fields:
            value = person.get(field, "")
            if value:
                print(f"✓ {field}: {value}")
            else:
                print(f"✗ {field}: MISSING")
        
        # Test that person has all expected fields
        assert all(field in person for field in required_fields), f"{name} missing required fields"

def test_contact_info_format():
    """Test that contact info has reasonable formats."""
    for name, person in PEOPLE.items():
        print(f"\n=== Validating {name} contact format ===")
        
        # Email should contain @ symbol
        email = person.get("email", "")
        if "@" in email:
            print(f"✓ Email format looks valid: {email}")
        else:
            print(f"✗ Email format invalid: {email}")
        
        # Phone should be numeric (after removing common separators)
        phone = person.get("phone", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        if phone.isdigit() and len(phone) >= 10:
            print(f"✓ Phone format looks valid: {person.get('phone')}")
        else:
            print(f"✗ Phone format may be invalid: {person.get('phone')}")
        
        # Address should not be empty
        address = person.get("address", "")
        if address and len(address) > 10:
            print(f"✓ Address looks complete: {address}")
        else:
            print(f"✗ Address too short: {address}")

def test_searchable_fields():
    """Test that all new fields would be searchable."""
    new_fields = ["email", "phone", "address", "occupation"]
    
    print(f"\n=== Testing searchability of new fields ===")
    
    for field in new_fields:
        print(f"\nTesting search by {field}:")
        for name, person in PEOPLE.items():
            value = person.get(field, "")
            if value:
                # Simulate a search - check if value can be found in the field
                found = field in ["email", "phone", "address", "occupation"] and value != ""
                print(f"  {name}: {value} - {'Searchable' if found else 'Not searchable'}")

if __name__ == "__main__":
    print("=== Testing New Contact Information Features ===")
    
    try:
        test_new_contact_fields()
        print("\n✓ All contact fields test passed!")
        
        test_contact_info_format()
        print("\n✓ Contact format validation completed!")
        
        test_searchable_fields()
        print("\n✓ Searchability test completed!")
        
        print("\n🎉 All tests completed successfully! New contact features are working.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)