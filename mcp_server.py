from mcp.server.fastmcp import FastMCP
import random

# Khởi tạo server
mcp = FastMCP("info")

PEOPLE = {
    "Hang": {
        "age": 18,
        "birthday": "25/10",
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

ZODIAC_RANGES = [
    ((3, 21), (4, 19), "Bạch Dương"),
    ((4, 20), (5, 20), "Kim Ngưu"),
    ((5, 21), (6, 20), "Song Tử"),
    ((6, 21), (7, 22), "Cự Giải"),
    ((7, 23), (8, 22), "Sư Tử"),
    ((8, 23), (9, 22), "Xử Nữ"),
    ((9, 23), (10, 22), "Thiên Bình"),
    ((10, 23), (11, 21), "Bọ Cạp"),
    ((11, 22), (12, 21), "Nhân Mã"),
    ((12, 22), (1, 19), "Ma Kết"),
    ((1, 20), (2, 18), "Bảo Bình"),
    ((2, 19), (3, 20), "Song Ngư"),
]

ZODIAC_ELEMENT = {
    "Bạch Dương": "Lửa",
    "Sư Tử": "Lửa",
    "Nhân Mã": "Lửa",
    "Kim Ngưu": "Đất",
    "Xử Nữ": "Đất",
    "Ma Kết": "Đất",
    "Song Tử": "Khí",
    "Thiên Bình": "Khí",
    "Bảo Bình": "Khí",
    "Cự Giải": "Nước",
    "Bọ Cạp": "Nước",
    "Song Ngư": "Nước",
}

COMPLEMENT_ELEMENTS = {
    "Lửa": "Khí",
    "Khí": "Lửa",
    "Đất": "Nước",
    "Nước": "Đất",
}


def normalize_name(name: str) -> str:
    return name.strip().lower()


def find_person_key(name: str):
    needle = normalize_name(name)
    for key in PEOPLE:
        if key.lower() in needle:
            return key
    return None


def zodiac_from_birthday(birthday: str) -> str:
    try:
        day_str, month_str = birthday.split("/")
        day = int(day_str)
        month = int(month_str)
    except ValueError:
        return "Không rõ"

    for start, end, zodiac in ZODIAC_RANGES:
        if start[0] <= month <= end[0]:
            if start[0] == end[0]:
                if start[1] <= day <= end[1]:
                    return zodiac
            elif month == start[0] and day >= start[1]:
                return zodiac
            elif month == end[0] and day <= end[1]:
                return zodiac
    return "Không rõ"


def build_profile(name: str):
    person = PEOPLE[name]
    zodiac = zodiac_from_birthday(person["birthday"])
    return {
        "name": name,
        "age": person["age"],
        "birthday": person["birthday"],
        "zodiac": zodiac,
        "family": person["family"],
        "hobby": person["hobby"],
        "quote": person["quote"],
        "favorite_color": person["favorite_color"],
    }


@mcp.tool()
def get_info(name: str):
    """
    Get info of name includes: age, birthday, zodiac
    """
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "age": person["age"],
            "birthday": person["birthday"],
            "zodiac": zodiac_from_birthday(person["birthday"]),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_people_family(name: str):
    """
    Get name of all people in family follow name
    """
    key = find_person_key(name)
    if key:
        return PEOPLE[key]["family"]
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_profile(name: str):
    """
    Get full profile: info + family + hobby + quote + favorite color
    """
    key = find_person_key(name)
    if key:
        return build_profile(key)
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_random_person():
    """
    Get a random person profile
    """
    key = random.choice(list(PEOPLE.keys()))
    return build_profile(key)


@mcp.tool()
def get_compatibility(name_a: str, name_b: str):
    """
    Simple compatibility check between two people
    """
    key_a = find_person_key(name_a)
    key_b = find_person_key(name_b)
    if not key_a or not key_b:
        return "Không có dữ liệu được lưu trữ"

    profile_a = build_profile(key_a)
    profile_b = build_profile(key_b)
    element_a = ZODIAC_ELEMENT.get(profile_a["zodiac"], "")
    element_b = ZODIAC_ELEMENT.get(profile_b["zodiac"], "")

    if element_a and element_b:
        if element_a == element_b:
            score = 90
            note = "Cùng nguyên tố, dễ đồng điệu."
        elif COMPLEMENT_ELEMENTS.get(element_a) == element_b:
            score = 80
            note = "Nguyên tố bổ trợ, khá hòa hợp."
        else:
            score = 60
            note = "Khác nguyên tố, cần thấu hiểu nhiều hơn."
    else:
        score = 70
        note = "Thiếu dữ liệu cung hoàng đạo, tạm đánh giá trung bình."

    lucky_color = f"{profile_a['favorite_color']} & {profile_b['favorite_color']}"

    return {
        "person_a": profile_a["name"],
        "person_b": profile_b["name"],
        "zodiac_a": profile_a["zodiac"],
        "zodiac_b": profile_b["zodiac"],
        "compatibility_score": score,
        "note": note,
        "lucky_color": lucky_color,
    }


# if __name__ == "__main__":
#     # Chỉ cần run trực tiếp, FastMCP Cloud sẽ quản lý asyncio loop
#     mcp.run(transport="sse")
