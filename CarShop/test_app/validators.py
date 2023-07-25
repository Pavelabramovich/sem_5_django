import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator

PHONE_PATTERN = r"\+375\s*\(\s*29\s*\)\s*\d{3}\s*-\s*\d{2}\s*-\s*\d{2}"

WORD_PATTERN = r"\b([A-Za-z]+)\b"
NUMBER_PATTERN = r"\b([\d\.\-]+)\b"

ADDRESS_PATTERN = fr"(({WORD_PATTERN})|({NUMBER_PATTERN})|([\s,\.\:\!]*))*"


# Check is string represent phone number in format
# +375 (29) XXX-XX-XX; using some pattern
def is_phone_number(string: str):
    if not isinstance(string, str):
        return False

    string = string.strip()
    match = re.fullmatch(PHONE_PATTERN, string)
    return match is not None


# Checks the composition of strings from words and numbers
def is_address(string: str):
    if not isinstance(string, str):
        return False

    string = string.strip()
    match = re.fullmatch(ADDRESS_PATTERN, string)
    return match is not None


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _("%(value)s is not an even number"),
            params={"value": value},
        )


class FullMatchRegexValidator(RegexValidator):
    def __init__(
            self, pattern, message=None, code=None, inverse_match=None, flags=None
    ):
        if not isinstance(pattern, str):
            raise TypeError("Pattern must be string.")

        if not pattern.startswith('^'):
            pattern = '^' + pattern

        if not pattern.endswith('$'):
            pattern += '$'

        super().__init__(
            pattern,
            message,
            code,
            inverse_match,
            flags
        )


validate_phone_number = FullMatchRegexValidator(
    PHONE_PATTERN,
    "Phone number is incorrect. Correct format is +375 (29) XXX-XX-XX.",
    code="invalid"
)

validate_address = FullMatchRegexValidator(
    ADDRESS_PATTERN,
    "Address is incorrect. It must consist of words, numbers and codes.",
    code="invalid"
)


def validate_non_negative(value_name):
    return MinValueValidator(limit_value=0, message=f"{value_name} must be not negative.")


def validate_positive(value_name):
    return MinValueValidator(limit_value=1, message=f"{value_name} must be positive.")
