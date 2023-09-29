import datetime
import re

from fuzzywuzzy import fuzz
from dateutil.parser import parse as parse_date


class LevenshteinStringMatcher:
    def __init__(self, flag=None):
        match flag:
            # In the entire second string we are looking for a match with the first
            case "partial":
                self.comp_func = fuzz.partial_ratio
            # Word comparison
            case "token sort":
                self.comp_func = fuzz.token_sort_ratio
            # Partial (see partial case) comparison by words
            case "partial token sort":
                self.comp_func = fuzz.partial_token_sort_ratio
            # Comparison on a set of words.
            case "token set":
                self.comp_func = fuzz.token_set_ratio
            # Partial comparison on a set of words.
            case "partial token set":
                self.comp_func = fuzz.partial_token_set_ratio
            # Full match
            case "full":
                self.comp_func = lambda f, s: (f == s) * 100
            # How much do the strings match
            case _:
                self.comp_func = fuzz.ratio

    # Returns the proportion of matching strings from 0 to 1.
    def __call__(self, first, second):
        return self.comp_func(first, second) / 100


match_address = LevenshteinStringMatcher(flag="token sort")


def match_phone_number(phone_number, string):
    phone_numbers_in_string = re.findall(r"(\d[\d\s()-]*\d)|\d", string)
    string_digits = [re.findall(r"\d", digits) for digits in phone_numbers_in_string]

    phone_number_digits = re.findall(r"\d", phone_number)

    # Maximum match length when searching for first in second.
    def longest_match_len(first, second):
        maximum = 0

        for start_second in range(len(second)):

            if start_second + maximum >= len(second):
                break

            sub_max = 0

            for bias in range(len(first)):
                if start_second + bias < len(second) and second[start_second + bias] == first[bias]:
                    sub_max += 1
                else:
                    break

            if maximum < sub_max:
                maximum = sub_max

        return maximum

    tmp_max = 0

    for number in string_digits:
        m = longest_match_len(phone_number_digits, number)
        if m > tmp_max:
            tmp_max = m

    return round(tmp_max / len(phone_number_digits), 2)


def match_date(date, string):
    try:
        if isinstance(date, str):
            try:
                date = parse_date(date).date()
            except ValueError:
                return 0.0

        elif isinstance(date, datetime.datetime):
            date = date.date()

        elif not isinstance(date, datetime.date):
            raise ValueError("Date must be date, datetime or string with date")

        # parse function from dateutil treats a number as the day of the current month and year
        try:
            int(string)
            return 0
        except ValueError:
            pass

        string_date = parse_date(string).date()

        score = 0

        year_match_scores = 17 / 32
        month_match_scores = 10 / 32
        day_match_scores = 1 - year_match_scores - month_match_scores

        if string_date.year == date.year:
            score += year_match_scores
        else:
            return score

        if string_date.month == date.month:
            score += month_match_scores
        else:
            return round(score, 2)

        if string_date.day == date.day:
            score += day_match_scores
        else:
            return round(score, 2)

        return round(score, 2)

    except ValueError:
        return 0


match_content = LevenshteinStringMatcher(flag="partial token set")
