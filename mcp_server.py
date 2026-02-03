from mcp.server.fastmcp import FastMCP
import random
import re
import unicodedata
from datetime import datetime
from typing import List, Optional

try:
    # Python 3.9+
    from zoneinfo import ZoneInfo  # type: ignore
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

# Khởi tạo server
mcp = FastMCP("info")

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


def normalize_text(text: str) -> str:
    """Normalize text for forgiving comparisons (case-insensitive, no accents)."""
    if text is None:
        return ""
    s = str(text).strip().lower()
    # Remove Vietnamese accents/diacritics for more forgiving search
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    # Normalize whitespace
    s = re.sub(r"\s+", " ", s)
    return s


def _normalize_city_text(text: str) -> str:
    if text is None:
        return ""
    normalized = normalize_text(text)
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _extract_city_from_address(address: str) -> str:
    if not address:
        return ""
    parts = [p.strip() for p in str(address).split(",") if p.strip()]
    if not parts:
        return ""
    if len(parts) >= 2:
        last_norm = normalize_text(parts[-1])
        if last_norm in {"viet nam", "vietnam"}:
            return parts[-2]
    return parts[-1]


def find_person_key(name: str):
    needle = normalize_name(name)
    for key in PEOPLE:
        if key.lower() in needle:
            return key
    return None


RELATION_ALIASES = {
    # Parents
    "father": "father",
    "dad": "father",
    "cha": "father",
    "bố": "father",
    "ba": "father",
    "bố ruột": "father",
    "cha ruột": "father",
    "bố đẻ": "father",
    "cha đẻ": "father",
    "bố của": "father",
    "cha của": "father",
    # Mother
    "mother": "mother",
    "mom": "mother",
    "mẹ": "mother",
    "má": "mother",
    "mẹ ruột": "mother",
    "mẹ đẻ": "mother",
    "mẹ của": "mother",
    # Siblings
    "brother": "brother",
    "anh": "brother",
    "anh trai": "brother",
    "em trai": "brother",
    "chị": "sister",
    "chị gái": "sister",
    "em gái": "sister",
    "sister": "sister",
}


def normalize_relation(
    relation: str, *, available_relations: Optional[List[str]] = None
) -> str:
    """Normalize a human relation string to our canonical keys.

    Canonical keys used in PEOPLE[*]["family"] currently include: father, mother,
    brother, sister.

    If the user provides a generic sibling term like "em" and only one sibling
    relation exists in the available_relations, we will infer that relation.
    """

    if not relation:
        return ""

    r = relation.strip().lower()

    # quick alias mapping
    if r in RELATION_ALIASES:
        return RELATION_ALIASES[r]

    # common generic sibling terms
    if r in {"em", "anh chị em", "anh chi em", "sibling", "siblings"} and available_relations:
        sibling_keys = [k for k in available_relations if k in {"brother", "sister"}]
        if len(sibling_keys) == 1:
            return sibling_keys[0]

    # fall back to raw input (may already be canonical)
    return r


_BIRTHDAY_RE = re.compile(r"^\s*(\d{1,2})\s*[/\-.]\s*(\d{1,2})\s*$")


def parse_birthday_day_month(birthday: str) -> Optional[tuple[int, int]]:
    """Parse birthday string like 'dd/mm' into (day, month).

    Accepts separators: '/', '-', '.' and tolerates surrounding spaces.
    Returns None if invalid/unsupported.
    """

    if not birthday:
        return None

    m = _BIRTHDAY_RE.match(birthday)
    if not m:
        return None

    day = int(m.group(1))
    month = int(m.group(2))

    if not (1 <= month <= 12):
        return None
    if not (1 <= day <= 31):
        return None

    # Allow Feb 29 (no year info); reject obviously invalid dates like 31/04.
    max_day_by_month = {
        1: 31,
        2: 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }

    if day > max_day_by_month[month]:
        return None

    return day, month


def format_birthday_ddmm(birthday: str) -> str:
    """Normalize birthday string to dd/mm format when possible."""
    if birthday is None:
        return ""

    birthday_text = str(birthday).strip()
    parsed = parse_birthday_day_month(birthday_text)
    if not parsed:
        return birthday_text

    day, month = parsed
    return f"{day:02d}/{month:02d}"


def zodiac_from_birthday(birthday: str) -> str:
    parsed = parse_birthday_day_month(birthday)
    if not parsed:
        return "Không rõ"

    day, month = parsed
    key = month * 100 + day

    for start, end, zodiac in ZODIAC_RANGES:
        start_key = start[0] * 100 + start[1]
        end_key = end[0] * 100 + end[1]

        if start_key <= end_key:
            if start_key <= key <= end_key:
                return zodiac
        else:
            # Range wraps over the new year (e.g. 12/22 -> 1/19)
            if key >= start_key or key <= end_key:
                return zodiac

    return "Không rõ"


def zodiac_number_from_birthday(birthday: str) -> Optional[int]:
    """Return zodiac number 1-12 based on ZODIAC_RANGES order."""

    zodiac = zodiac_from_birthday(birthday)
    if zodiac == "Không rõ":
        return None

    for i, (_, _, name) in enumerate(ZODIAC_RANGES, start=1):
        if name == zodiac:
            return i

    return None


def zodiac_info_from_birthday(birthday: str):
    zodiac = zodiac_from_birthday(birthday)
    zodiac_number = zodiac_number_from_birthday(birthday)
    return {"zodiac": zodiac, "zodiac_number": zodiac_number}


def build_profile(name: str):
    person = PEOPLE[name]
    zodiac_info = zodiac_info_from_birthday(person["birthday"])
    return {
        "name": name,
        "age": person["age"],
        "birthday": person["birthday"],
        "zodiac": zodiac_info["zodiac"],
        "zodiac_number": zodiac_info["zodiac_number"],
        "work_experience_years": person.get("work_experience_years", 0),
        "email": person.get("email", ""),
        "phone": person.get("phone", ""),
        "address": person.get("address", ""),
        "occupation": person.get("occupation", ""),
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
        zodiac_info = zodiac_info_from_birthday(person["birthday"])
        return {
            "age": person["age"],
            "birthday": person["birthday"],
            "zodiac": zodiac_info["zodiac"],
            "zodiac_number": zodiac_info["zodiac_number"],
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_birthday(name: str):
    """Trả về ngày sinh theo định dạng dd/mm."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "birthday": format_birthday_ddmm(person.get("birthday", "")),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_zodiac_number(birthday: str):
    """Get zodiac name and zodiac number (1-12) from a birthday string (dd/mm)."""

    info = zodiac_info_from_birthday(birthday)
    return {"birthday": birthday, **info}


@mcp.tool()
def get_work_experience_years(name: str):
    """Get number of working experience years for a person."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "work_experience_years": person.get("work_experience_years", 0),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_people_family(name: str):
    """Get raw family mapping for a person.

    Returns a dict of relation -> name (e.g., father/mother/brother/sister).
    """
    key = find_person_key(name)
    if key:
        return PEOPLE[key]["family"]
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_family_info(name: str):
    """Get family information of a person (members list + count).

    Returns:
    - person: canonical person key
    - members: list[{relation, name}]
    - member_count: number of family members stored
    """
    key = find_person_key(name)
    if key:
        family = PEOPLE[key]["family"]
        return {
            "person": key,
            "members": [
                {"relation": relation, "name": member}
                for relation, member in family.items()
            ],
            "member_count": len(family),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_family_overview(name: str):
    """Get a convenient family overview for a person.

    Useful for questions like:
    - "Gia đình của Hang gồm những ai?"
    - "Các mối quan hệ trong gia đình Minh là gì?"

    Returns:
    - person: canonical person key
    - family: raw mapping (relation -> name)
    - relations: list of relation keys
    - members: list[{relation, name}] (easy to render)
    - member_count: number of family members stored
    """

    key = find_person_key(name)
    if key:
        family = PEOPLE[key]["family"]
        return {
            "person": key,
            "family": family,
            "relations": list(family.keys()),
            "members": [
                {"relation": relation, "name": member}
                for relation, member in family.items()
            ],
            "member_count": len(family),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_family_member(name: str, relation: str):
    """Get a specific family member by relation.

    Example queries:
    - "Bố của Hang là ai?" (relation="bố")
    - "Mẹ Minh là ai?" (relation="mẹ")
    - "Anh/chị/em của Minh là ai?" (relation="em")

    Notes:
    - This tool normalizes Vietnamese/English relation aliases into canonical keys:
      father, mother, brother, sister.
    """

    key = find_person_key(name)
    if not key:
        return "Không có dữ liệu được lưu trữ"

    family = PEOPLE[key]["family"]
    available_relations = list(family.keys())
    resolved_relation = normalize_relation(relation, available_relations=available_relations)

    if resolved_relation in family:
        return {
            "person": key,
            "relation_requested": relation,
            "relation": resolved_relation,
            "name": family[resolved_relation],
        }

    # fallback: if the provided text contains a canonical key
    for rel in available_relations:
        if rel in relation.strip().lower():
            return {
                "person": key,
                "relation_requested": relation,
                "relation": rel,
                "name": family[rel],
            }

    return {
        "person": key,
        "relation_requested": relation,
        "message": "Không tìm thấy quan hệ trong dữ liệu gia đình.",
        "available_relations": available_relations,
    }


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
def get_contact_info(name: str):
    """Get contact information (email, phone, address) for a person."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "email": person.get("email", ""),
            "phone": person.get("phone", ""),
            "address": person.get("address", ""),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_email(name: str):
    """Get email address of a person."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "email": person.get("email", ""),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_phone(name: str):
    """Get phone number of a person."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "phone": person.get("phone", ""),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def get_address(name: str):
    """Get home address of a person."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "address": person.get("address", ""),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def find_people_by_city(city: str, include_profiles: bool = False, limit: int = 10):
    """Find people by city extracted from their address."""
    if city is None:
        return {
            "city": "",
            "normalized_city": "",
            "count": 0,
            "people": [],
        }

    city_norm = _normalize_city_text(city)
    if not city_norm:
        return {
            "city": city,
            "normalized_city": "",
            "count": 0,
            "people": [],
        }

    try:
        limit_i = int(limit)
    except Exception:
        limit_i = 10
    if limit_i <= 0:
        limit_i = 10
    limit_i = min(limit_i, 50)

    matches = []
    for name in sorted(PEOPLE.keys()):
        profile = build_profile(name)
        address = profile.get("address", "")
        city_from_address = _extract_city_from_address(address)
        city_from_address_norm = _normalize_city_text(city_from_address)
        if not city_from_address_norm:
            continue
        if city_norm not in city_from_address_norm:
            continue
        matches.append(profile if include_profiles else name)
        if len(matches) >= limit_i:
            break

    return {
        "city": city,
        "normalized_city": city_norm,
        "count": len(matches),
        "limit": limit_i,
        "people": matches,
    }


@mcp.tool()
def update_person(name: str, field: str, new_value: str):
    """Cập nhật email/phone/address cho người đã có."""
    key = find_person_key(name)
    if not key:
        return "Không có dữ liệu được lưu trữ"

    normalized_field = normalize_text(field)
    field_aliases = {
        "email": "email",
        "e mail": "email",
        "e-mail": "email",
        "mail": "email",
        "phone": "phone",
        "phone number": "phone",
        "sdt": "phone",
        "so dt": "phone",
        "so dien thoai": "phone",
        "dien thoai": "phone",
        "address": "address",
        "dia chi": "address",
        "dc": "address",
    }
    field_key = field_aliases.get(normalized_field)
    if not field_key:
        return {
            "message": "Trường cần cập nhật không hợp lệ.",
            "field": field,
            "allowed_fields": ["email", "phone", "address"],
        }

    value = "" if new_value is None else str(new_value).strip()
    if not value:
        return {"message": "Giá trị mới không hợp lệ.", "field": field_key}

    person = PEOPLE[key]
    old_value = person.get(field_key, "")
    person[field_key] = value

    return {
        "person": key,
        "field": field_key,
        "old_value": old_value,
        "new_value": value,
        "contact_info": {
            "email": person.get("email", ""),
            "phone": person.get("phone", ""),
            "address": person.get("address", ""),
        },
    }


@mcp.tool()
def get_occupation(name: str):
    """Get occupation/job of a person."""
    key = find_person_key(name)
    if key:
        person = PEOPLE[key]
        return {
            "person": key,
            "occupation": person.get("occupation", ""),
        }
    return "Không có dữ liệu được lưu trữ"


@mcp.tool()
def add_person(
    name: str,
    age: int,
    birthday: str,
    email: str = "",
    phone: str = "",
    address: str = "",
    occupation: str = "",
    work_experience_years: int = 0,
    family: Optional[dict] = None,
    hobby: str = "",
    quote: str = "",
    favorite_color: str = "",
):
    """Thêm người mới vào hệ thống."""
    cleaned_name = str(name).strip()
    if not cleaned_name:
        return "Tên không hợp lệ"

    normalized_name = normalize_name(cleaned_name)
    for existing in PEOPLE:
        if normalize_name(existing) == normalized_name:
            return {
                "message": "Người đã tồn tại trong hệ thống.",
                "person": existing,
            }

    birthday_value = str(birthday).strip()
    if not birthday_value:
        return {
            "message": "Ngày sinh không hợp lệ. Vui lòng dùng định dạng dd/mm.",
            "birthday": birthday,
        }

    if parse_birthday_day_month(birthday_value) is None:
        return {
            "message": "Ngày sinh không hợp lệ. Vui lòng dùng định dạng dd/mm.",
            "birthday": birthday_value,
        }

    try:
        age_value = int(age)
    except Exception:
        return {"message": "Tuổi không hợp lệ.", "age": age}

    try:
        work_years_value = int(work_experience_years)
    except Exception:
        work_years_value = 0

    family_value = family if isinstance(family, dict) else None
    if family is not None and family_value is None:
        return {"message": "Family phải là dict quan hệ -> tên.", "family": family}

    PEOPLE[cleaned_name] = {
        "age": age_value,
        "birthday": birthday_value,
        "work_experience_years": work_years_value,
        "email": str(email).strip(),
        "phone": str(phone).strip(),
        "address": str(address).strip(),
        "occupation": str(occupation).strip(),
        "family": family_value or {},
        "hobby": str(hobby).strip(),
        "quote": str(quote).strip(),
        "favorite_color": str(favorite_color).strip(),
    }

    return {
        "added": cleaned_name,
        "profile": build_profile(cleaned_name),
        "count": len(PEOPLE),
    }


@mcp.tool()
def list_people(include_profiles: bool = False):
    """List all people currently stored.

    Args:
        include_profiles: If True, return full profiles for each person.

    Returns:
        Dict with:
        - count: number of people
        - people: list of names or list of profiles
    """

    names = sorted(PEOPLE.keys())

    if include_profiles:
        return {"count": len(names), "people": [build_profile(name) for name in names]}

    return {"count": len(names), "people": names}


@mcp.tool()
def delete_person(name: str):
    """Xóa người khỏi hệ thống theo tên."""
    key = find_person_key(name)
    if not key:
        return "Không có dữ liệu được lưu trữ"

    profile = build_profile(key)
    PEOPLE.pop(key, None)

    deleted_norm = normalize_text(key)
    for person in PEOPLE.values():
        family = person.get("family")
        if not isinstance(family, dict):
            continue
        for relation, member in list(family.items()):
            if normalize_text(member) == deleted_norm:
                family.pop(relation, None)

    return {
        "deleted": key,
        "profile": profile,
        "remaining_count": len(PEOPLE),
    }


SEARCHABLE_FIELDS = {
    "name",
    "age",
    "birthday",
    "zodiac",
    "zodiac_number",
    "work_experience_years",
    "email",
    "phone",
    "address",
    "occupation",
    "hobby",
    "quote",
    "favorite_color",
    "family",
}


def _normalize_fields(fields: Optional[List[str]]) -> Optional[List[str]]:
    if not fields:
        return None
    out: List[str] = []
    for f in fields:
        if not f:
            continue
        k = str(f).strip().lower()
        if k in SEARCHABLE_FIELDS:
            out.append(k)
    return out or None


def _normalize_sort_field(sort_by: Optional[str]) -> Optional[str]:
    if not sort_by:
        return None
    key = str(sort_by).strip().lower()
    return key if key in SEARCHABLE_FIELDS else None


def _coerce_number(value) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except Exception:
        return None


def _match_filter_value(field_value, criteria) -> bool:
    if criteria is None:
        return True

    if isinstance(criteria, (list, tuple, set)):
        return any(_match_filter_value(field_value, item) for item in criteria)

    if isinstance(criteria, dict):
        numeric_value = _coerce_number(field_value)
        min_value = criteria.get("min")
        max_value = criteria.get("max")
        exact_value = criteria.get("value")

        if numeric_value is not None and (min_value is not None or max_value is not None):
            if min_value is not None:
                min_number = _coerce_number(min_value)
                if min_number is not None and numeric_value < min_number:
                    return False
            if max_value is not None:
                max_number = _coerce_number(max_value)
                if max_number is not None and numeric_value > max_number:
                    return False
            return True

        if exact_value is not None:
            return _match_filter_value(field_value, exact_value)

        # If no valid range/value provided, treat as non-match.
        return False

    numeric_value = _coerce_number(field_value)
    numeric_criteria = _coerce_number(criteria)
    if numeric_value is not None and numeric_criteria is not None:
        return numeric_value == numeric_criteria

    hay = normalize_text(field_value)
    needle = normalize_text(criteria)
    if needle == "":
        return True
    return needle in hay


def _normalize_filters(filters: Optional[dict]) -> Optional[dict]:
    if not filters or not isinstance(filters, dict):
        return None
    applied: dict = {}
    for key, criteria in filters.items():
        if not key:
            continue
        field_key = str(key).strip().lower()
        if field_key in SEARCHABLE_FIELDS:
            applied[field_key] = criteria
    return applied or None


def _apply_filters(field_value_map: dict, filters: Optional[dict]) -> bool:
    if not filters:
        return True
    for key, criteria in filters.items():
        if not _match_filter_value(field_value_map.get(key, ""), criteria):
            return False
    return True


def _sort_value(raw_value):
    if raw_value is None:
        return (1, "")
    numeric_value = _coerce_number(raw_value)
    if numeric_value is not None:
        return (0, numeric_value)
    return (0, normalize_text(raw_value))


def _collect_suggestions(
    query: str,
    profile_entries: List[dict],
    fields: Optional[List[str]],
    limit: int,
) -> List[str]:
    needle = normalize_text(query)
    if needle == "":
        return []

    try:
        limit_i = int(limit)
    except Exception:
        limit_i = 5
    if limit_i <= 0:
        limit_i = 5
    limit_i = min(limit_i, 20)

    fields_to_use = fields or list(SEARCHABLE_FIELDS)
    suggestions: List[str] = []
    seen = set()

    for entry in profile_entries:
        field_value_map = entry.get("fields", {})
        for field in fields_to_use:
            raw_value = field_value_map.get(field, "")
            if raw_value is None:
                continue
            candidate = str(raw_value).strip()
            if not candidate:
                continue
            candidate_norm = normalize_text(candidate)
            if needle in candidate_norm and candidate_norm != needle and candidate_norm not in seen:
                seen.add(candidate_norm)
                suggestions.append(candidate)
                if len(suggestions) >= limit_i:
                    return suggestions

    return suggestions


@mcp.tool()
def search_people(
    query: str,
    fields: Optional[List[str]] = None,
    include_profiles: bool = False,
    limit: int = 10,
    filters: Optional[dict] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    suggest_limit: int = 5,
    suggest_fields: Optional[List[str]] = None,
):
    """Search people by a free-text query.

    - Mặc định sẽ search trên tất cả field phổ biến (name, hobby, quote, ...).
    - Search không phân biệt hoa/thường và có hỗ trợ bỏ dấu (để match dễ hơn).
    - Hỗ trợ lọc theo field, sắp xếp kết quả và gợi ý từ khóa.

    Args:
        query: Chuỗi cần tìm.
        fields: Danh sách field muốn search (vd: ["name", "hobby"]). Nếu None -> search all.
        include_profiles: True -> trả về full profile; False -> chỉ trả về danh sách tên.
        limit: Giới hạn số kết quả trả về.
        filters: Dict field -> giá trị lọc (vd: {"age": 18} hoặc {"age": {"min": 18}}).
        sort_by: Field cần sắp xếp (vd: "age", "name").
        sort_order: "asc" hoặc "desc".
        suggest_limit: Giới hạn số gợi ý từ khóa.
        suggest_fields: Field dùng để gợi ý (mặc định theo fields/searchable).

    Returns:
        Dict gồm query, count, people, matches, filters, sort_by, sort_order, suggestions.
    """

    needle = normalize_text(query)
    normalized_fields = _normalize_fields(fields)
    normalized_filters = _normalize_filters(filters)
    sort_field = _normalize_sort_field(sort_by)
    suggest_fields_norm = _normalize_fields(suggest_fields) or normalized_fields

    # clamp limit to avoid returning too much data
    try:
        limit_i = int(limit)
    except Exception:
        limit_i = 10
    if limit_i <= 0:
        limit_i = 10
    limit_i = min(limit_i, 50)

    sort_order_norm = str(sort_order).strip().lower() if sort_order is not None else "asc"
    sort_desc = sort_order_norm in {"desc", "descending", "giam", "giam dan", "giamdan"}

    matches: List[dict] = []
    profile_entries: List[dict] = []
    fields_to_search = normalized_fields or list(SEARCHABLE_FIELDS)

    for name in sorted(PEOPLE.keys()):
        profile = build_profile(name)

        # Build searchable text per field
        family = profile.get("family") or {}
        family_text = " ".join(f"{rel} {member}" for rel, member in family.items())

        field_value_map = {
            "name": profile.get("name", ""),
            "age": profile.get("age", ""),
            "birthday": profile.get("birthday", ""),
            "zodiac": profile.get("zodiac", ""),
            "zodiac_number": profile.get("zodiac_number", ""),
            "work_experience_years": profile.get("work_experience_years", ""),
            "email": profile.get("email", ""),
            "phone": profile.get("phone", ""),
            "address": profile.get("address", ""),
            "occupation": profile.get("occupation", ""),
            "hobby": profile.get("hobby", ""),
            "quote": profile.get("quote", ""),
            "favorite_color": profile.get("favorite_color", ""),
            "family": family_text,
        }

        profile_entries.append({"profile": profile, "fields": field_value_map})

        matched_fields: List[str] = []

        # If empty query -> treat as match-all (like list_people) but still respects limit
        if needle == "":
            matched_fields = fields_to_search
        else:
            for f in fields_to_search:
                hay = normalize_text(field_value_map.get(f, ""))
                if needle and needle in hay:
                    matched_fields.append(f)

        if not matched_fields:
            continue

        if not _apply_filters(field_value_map, normalized_filters):
            continue

        matches.append({
            "name": name,
            "matched_fields": sorted(set(matched_fields)),
            "profile": profile,
            "fields": field_value_map,
        })

    if sort_field:
        matches.sort(key=lambda m: _sort_value(m["fields"].get(sort_field)), reverse=sort_desc)

    matches = matches[:limit_i]

    if include_profiles:
        people_out = [m["profile"] for m in matches]
    else:
        people_out = [m["name"] for m in matches]

    suggestions = _collect_suggestions(query, profile_entries, suggest_fields_norm, suggest_limit)

    return {
        "query": query,
        "fields": normalized_fields or sorted(SEARCHABLE_FIELDS),
        "filters": normalized_filters or {},
        "sort_by": sort_field,
        "sort_order": sort_order_norm if sort_field else None,
        "count": len(matches),
        "limit": limit_i,
        "people": people_out,
        "matches": [
            {"name": m["name"], "matched_fields": m["matched_fields"]} for m in matches
        ],
        "suggestions": suggestions,
    }


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


@mcp.tool()
def health_check():
    """Simple health check for the MCP server."""
    now = datetime.now().astimezone()
    return {
        "status": "ok",
        "service": "info",
        "timestamp": now.isoformat(),
    }


@mcp.tool()
def get_current_time(tz: str = "Asia/Ho_Chi_Minh", fmt: str = "%Y-%m-%d %H:%M:%S"):
    """Lấy giờ hiện tại.

    Args:
        tz: Timezone IANA (vd: "Asia/Ho_Chi_Minh"). Nếu môi trường không hỗ trợ
            `zoneinfo` hoặc timezone không hợp lệ, sẽ fallback sang giờ local.
        fmt: Định dạng theo datetime.strftime.

    Returns:
        Dict gồm current_time (theo fmt) và iso (ISO-8601).
    """

    now: datetime

    if ZoneInfo is not None:
        try:
            now = datetime.now(ZoneInfo(tz))
        except Exception:
            now = datetime.now().astimezone()
            tz = str(now.tzinfo) if now.tzinfo else tz
    else:  # pragma: no cover
        now = datetime.now().astimezone()
        tz = str(now.tzinfo) if now.tzinfo else tz

    return {
        "timezone": tz,
        "current_time": now.strftime(fmt),
        "iso": now.isoformat(),
    }



# if __name__ == "__main__":
#     # Chỉ cần run trực tiếp, FastMCP Cloud sẽ quản lý asyncio loop
#     mcp.run(transport="sse")
