import re

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
