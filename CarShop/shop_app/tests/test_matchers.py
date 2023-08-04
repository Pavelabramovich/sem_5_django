from django.test import TestCase
from shop_app.matchers import \
    LevenshteinStringMatcher, \
    match_address, \
    match_phone_number, \
    match_date


class TestLevenshteinStringMatcher(TestCase):
    def test_normal(self):
        match_str = LevenshteinStringMatcher()
        first = "Hello world!"
        second = "Hillo woarld!"

        # Usual comparison. Since the words differ slightly, a high result is expected.
        expected_res = 0.85
        delta = 0.05

        res = match_str(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_partial(self):
        match_str = LevenshteinStringMatcher(flag='partial')
        first = "The log cabin is not visible from the sheep"
        second = """The log cabin is not visible from the ship. 
                    They must be aiming at a flag. We must load a flag advance."""

        # Partial comparison. Since the first sentence is contained
        # within the second with one change, a very high score is expected.
        expected_res = 0.95
        delta = 0.03

        res = match_str(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_token_sort(self):
        match_str = LevenshteinStringMatcher(flag='token sort')
        first = "It's the scariest thing in the world!"
        second = "The scariest thing in the world is..."

        # Sentences almost do not differ in words, a high result is expected
        expected_res = 0.95
        delta = 0.03

        res = match_str(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_partial_token_sort(self):
        match_str = LevenshteinStringMatcher(flag='partial token sort')
        first = "After all this time, always"
        second = "My parents always told me not to speak to."

        # Sentences have one word in common, low result is expected.
        expected_res = 0.35
        delta = 0.05

        res = match_str(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_token_set(self):
        match_str = LevenshteinStringMatcher(flag='token set')
        first = "one two three four three two one"
        second = "four one three two"

        # Sentences consist of the same set of words, a complete match is expected.
        expected_res = 1.0
        res = match_str(first, second)

        self.assertEqual(res, expected_res)

    def test_partial_token_set(self):
        match_str = LevenshteinStringMatcher(flag='partial token set')
        first = "one one one two three"
        second = "one two"

        # All words of one sentence are contained in another, expect a complete match.
        expected_res = 1.0
        res = match_str(first, second)

        self.assertEqual(res, expected_res)

    def test_full(self):
        match_str = LevenshteinStringMatcher(flag='full')
        first = "1234567890"
        second = "1234567891"

        # Strings are different, zero result expected
        expected_res = 0.0
        res = match_str(first, second)

        self.assertEqual(res, expected_res)


class TestAddressMatcher(TestCase):
    def test_normal(self):
        first = "6 Kings Road LLANDRINDOD WELLS"
        second = "Llandrindod wells, Kings road 6"

        # The address is the same, the word order is different, a complete match is expected.
        expected_res = 1.0
        res = match_address(first, second)

        self.assertEqual(res, expected_res)

    def test_partial(self):
        first = "55, London Road, Wakefield"
        second = "London Road"

        # One address is part of the second, an average result is expected..
        expected_res = 0.5
        delta = 0.15

        res = match_address(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_jumble(self):
        first = "235 Park Ave Floor 12"
        second = "SGeEgsefsezdf 3452 SEG sbSG"

        # Comparison with a letters jumble, low result expected.
        expected_res = 0.2
        delta = 0.05

        res = match_address(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)


class TestPhoneNumberMatcher(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_number = "+375 (29) 194-56-98"

    def test_normal(self):
        first = self.test_number
        second = "375 29 190 50 90"

        # Maximum matches 7 digits in a row of the 12, the expected result is 7/12.
        expected_res = 7/12
        delta = 0.01

        res = match_phone_number(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_in_text(self):
        first = self.test_number
        second = """
            zshzsr shzdra 2425 sgsa 375(29194-56    97  jkni
            tse 375 j 29 bibyi 194 kj - 56 98 szh z 
            +375szhsg g __ q4ssgzsgszsfagga kn (29) 194
            """

        # Maximum matches 11 digits in a row, expected result 11/12
        expected_res = 11/12
        delta = 0.01

        res = match_phone_number(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_no_blanks(self):
        first = self.test_number
        second = "375291945698"

        # Number exactly matches, exact match expected.
        expected_res = 1
        res = match_phone_number(first, second)

        self.assertEqual(res, expected_res)

    def test_no_digits(self):
        first = self.test_number
        second = "Where's the map, Billy?"

        # There are no digits in the string, zero result expected
        expected_res = 0
        res = match_phone_number(first, second)

        self.assertEqual(res, expected_res)

    def test_jumble(self):
        first = self.test_number
        second = "gszdesg 34 zsgag44 shasd  w32"

        # There are multiple digits in a string, a low result is expected.
        expected_res = 0.1
        delta = 0.05

        res = match_phone_number(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)


class TestDateMatcher(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_date = "18/10/2023"

    def test_normal(self):
        first = self.test_date
        second = "10/10/2023"

        # Dates differ only by day, high result expected
        expected_res = 0.8
        delta = 0.05

        res = match_date(first, second)

        self.assertAlmostEqual(res, expected_res, delta=delta)

    def test_incorrect(self):
        first = self.test_date
        second = "40-10-2023"

        # Date incorrect, zero result expected
        expected_res = 0.0
        res = match_date(first, second)

        self.assertEqual(res, expected_res)

    def test_words(self):
        first = self.test_date
        second = "October 18, 2023"

        # Date are same, a complete match is expected.
        expected_res = 1.0
        res = match_date(first, second)

        self.assertEqual(res, expected_res)

    def test_abbreviation(self):
        first = self.test_date
        second = "18 Oct. 2023"

        # Date are same, a complete match is expected.
        expected_res = 1.0
        res = match_date(first, second)

        self.assertEqual(res, expected_res)

    def test_dots(self):
        first = self.test_date
        second = "18.10.2023"

        # Date are same, a complete match is expected.
        expected_res = 1.0
        res = match_date(first, second)

        self.assertEqual(res, expected_res)
