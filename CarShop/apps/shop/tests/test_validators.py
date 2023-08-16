from django.test import TestCase
from django.forms import ValidationError
from apps.core.test_tools import AssertNotRaisesMixin

from apps.shop.validators import \
    FullMatchRegexValidator, \
    validate_address, \
    validate_phone_number, \
    get_not_negative_validator, \
    get_positive_validator


class TestFullMatchRegexValidator(AssertNotRaisesMixin, TestCase):
    def test_normal(self):
        with self.assertNotRaises(ValidationError):
            pattern = r"abc[\d\s]+def"
            test_str = "abc2345676543def"
            validate = FullMatchRegexValidator(pattern, code='invalid')

            validate(test_str)

    def test_partial(self):
        with self.assertRaises(ValidationError):
            pattern = r"abc[\d\s]+def"
            test_str = "___abc1def___"
            validate = FullMatchRegexValidator(pattern, code='invalid')

            validate(test_str)

    def test_jumble(self):
        with self.assertRaises(ValidationError):
            pattern = r"a"
            test_str = "aaaaaaa\n\f\taaaaaaaa"
            validate = FullMatchRegexValidator(pattern, code='invalid')

            validate(test_str)


class TestAddressValidator(TestCase, AssertNotRaisesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_func = validate_address

    def test_normal(self):
        with self.assertNotRaises(ValidationError):
            test_str = "London, city Windy street 15"
            self.test_func(test_str)

    def test_jumble(self):
        with self.assertRaises(ValidationError):
            test_str = "hsdjh a3Q EWYW3AWTYHt 42y5 q"
            self.test_func(test_str)


class TestPhoneNumberValidator(TestCase, AssertNotRaisesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_func = validate_phone_number

    def test_normal(self):
        with self.assertNotRaises(ValidationError):
            test_str = "+375 (29) 654-34-98"
            self.test_func(test_str)

    def test_hyphen(self):
        with self.assertRaises(ValidationError):
            test_str = "+375 (28) 654-34 98"
            self.test_func(test_str)

    def test_many_blanks(self):
        with self.assertNotRaises(ValidationError):
            test_str = "+375  (   29  ) 544-  33   -   90"
            self.test_func(test_str)

    def test_only_digits(self):
        with self.assertRaises(ValidationError):
            test_str = "+375295443390"
            self.test_func(test_str)


class TestPositiveValidator(TestCase, AssertNotRaisesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_func = get_positive_validator('value')

    def test_positive(self):
        with self.assertNotRaises(ValidationError):
            self.test_func(10)

    def test_negative(self):
        with self.assertRaises(ValidationError):
            self.test_func(-10)

    def test_one(self):
        with self.assertNotRaises(ValidationError):
            self.test_func(1)

    def test_negative_one(self):
        with self.assertRaises(ValidationError):
            self.test_func(-1)

    def test_zero(self):
        with self.assertRaises(ValidationError):
            self.test_func(0)


class TestNotNegativeValidator(TestCase, AssertNotRaisesMixin):
    @classmethod
    def setUpTestData(cls):
        cls.test_func = get_not_negative_validator('value')

    def test_positive(self):
        with self.assertNotRaises(ValidationError):
            self.test_func(10)

    def test_negative(self):
        with self.assertRaises(ValidationError):
            self.test_func(-10)

    def test_one(self):
        with self.assertNotRaises(ValidationError):
            self.test_func(1)

    def test_negative_one(self):
        with self.assertRaises(ValidationError):
            self.test_func(-1)

    def test_zero(self):
        with self.assertNotRaises(ValidationError):
            self.test_func(0)
