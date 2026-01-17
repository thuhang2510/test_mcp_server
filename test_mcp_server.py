import unittest
from datetime import datetime

from mcp_server import (
    get_current_time,
    list_people,
    search_people,
    parse_birthday_day_month,
    zodiac_from_birthday,
    zodiac_info_from_birthday,
    zodiac_number_from_birthday,
)


class TestZodiacNumber(unittest.TestCase):
    def test_parse_birthday_accepts_multiple_separators(self):
        self.assertEqual(parse_birthday_day_month("09/04"), (9, 4))
        self.assertEqual(parse_birthday_day_month(" 9-4 "), (9, 4))
        self.assertEqual(parse_birthday_day_month("9.4"), (9, 4))

    def test_parse_birthday_rejects_invalid_dates(self):
        self.assertIsNone(parse_birthday_day_month("31/04"))  # April has 30 days
        self.assertIsNone(parse_birthday_day_month("00/01"))
        self.assertIsNone(parse_birthday_day_month("01/00"))
        self.assertIsNone(parse_birthday_day_month("abc"))

    def test_zodiac_boundaries_aries_taurus(self):
        self.assertEqual(zodiac_from_birthday("19/04"), "Bạch Dương")
        self.assertEqual(zodiac_number_from_birthday("19/04"), 1)

        self.assertEqual(zodiac_from_birthday("20/04"), "Kim Ngưu")
        self.assertEqual(zodiac_number_from_birthday("20/04"), 2)

    def test_zodiac_wrap_new_year_capricorn(self):
        # Ma Kết wraps across year end: 22/12 -> 19/01
        self.assertEqual(zodiac_from_birthday("22/12"), "Ma Kết")
        self.assertEqual(zodiac_number_from_birthday("22/12"), 10)

        self.assertEqual(zodiac_from_birthday("19/01"), "Ma Kết")
        self.assertEqual(zodiac_number_from_birthday("19/01"), 10)

        self.assertEqual(zodiac_from_birthday("20/01"), "Bảo Bình")
        self.assertEqual(zodiac_number_from_birthday("20/01"), 11)

    def test_zodiac_info(self):
        info = zodiac_info_from_birthday("29/02")
        self.assertEqual(info["zodiac"], "Song Ngư")
        self.assertEqual(info["zodiac_number"], 12)

    def test_unknown_on_invalid_input(self):
        self.assertEqual(zodiac_from_birthday("31/04"), "Không rõ")
        self.assertIsNone(zodiac_number_from_birthday("31/04"))

    def test_get_current_time_output(self):
        out = get_current_time(tz="UTC")
        self.assertIn("current_time", out)
        self.assertIn("iso", out)
        self.assertIn("timezone", out)

        # ISO string phải parse được
        datetime.fromisoformat(out["iso"])


class TestListPeople(unittest.TestCase):
    def test_list_people_names(self):
        out = list_people()

        self.assertIn("count", out)
        self.assertIn("people", out)
        self.assertEqual(out["count"], len(out["people"]))
        self.assertEqual(out["people"], sorted(out["people"]))

        self.assertIn("Hang", out["people"])
        self.assertIn("Minh", out["people"])

    def test_list_people_profiles(self):
        out = list_people(include_profiles=True)

        self.assertEqual(out["count"], len(out["people"]))
        names = {p["name"] for p in out["people"]}
        self.assertEqual(names, {"Hang", "Minh"})
        self.assertTrue(all("zodiac" in p for p in out["people"]))


class TestSearchPeople(unittest.TestCase):
    def test_search_by_name_case_insensitive(self):
        out = search_people("HANG")
        self.assertIn("people", out)
        self.assertIn("Hang", out["people"])

    def test_search_by_hobby_no_accents(self):
        out = search_people("nhiep anh", fields=["hobby"])
        self.assertEqual(out["people"], ["Hang"])

    def test_search_by_favorite_color(self):
        out = search_people("xanh", fields=["favorite_color"])
        self.assertEqual(out["people"], ["Minh"])

    def test_search_include_profiles(self):
        out = search_people("minh", include_profiles=True)
        self.assertEqual(out["count"], 1)
        self.assertEqual(out["people"][0]["name"], "Minh")
        self.assertIn("hobby", out["people"][0])

    def test_search_limit_on_empty_query(self):
        out = search_people("", limit=1)
        self.assertEqual(out["count"], 1)
        self.assertEqual(len(out["people"]), 1)


if __name__ == "__main__":
    unittest.main()
