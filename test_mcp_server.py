import unittest

from mcp_server import (
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


if __name__ == "__main__":
    unittest.main()
