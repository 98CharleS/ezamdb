from datetime import datetime
import re
from date_transform import transforming_to_datetime


def raw_date_stripping(date_str):  # takes date as a string, check if it is alright and returns bool valve
    try:
        # replace mixed separators with a standard one
        date_str = re.sub(r'[.\-]', '.', date_str)
        day, month, year = map(int, date_str.split('.'))
        # validate date using datetime
        datetime(year, month, day)
        return day, month, year
    except ValueError:
        print(f"{date_str} is an invalid date")
        return False


def is_first_date_lesser(raw_first_date, raw_second_date):
    try:
        # parse the input strings into datetime objects
        first_date = transforming_to_datetime(raw_first_date)
        second_date = transforming_to_datetime(raw_second_date)

        # compare the dates
        return first_date <= second_date
    except ValueError as e:
        print(f"Error: {e}")
        return None


def date_validation(first_date, second_date):
    return bool(raw_date_stripping(first_date) and raw_date_stripping(second_date))


def cpv_validation(cpv_code):  # validating if CPV code is right
    if not cpv_code:
        print("Please enter the CPV code")
        return False
    elif cpv_code == "all":
        return True
    elif re.fullmatch(r"\d{8}-\d", cpv_code):  # strict match
        return True
    else:
        print(f'"{cpv_code}" is not a valid CPV code.\n'
              f'A valid CPV code should consist of 8 digits, a dash, and 1 digit (e.g., 42111100-1).')
        return False


def validations(day_from, day_to, cpv):  # all validations in one place
    if not date_validation(day_from, day_to):
        print("One or both dates are invalid")
        return False
    if not is_first_date_lesser(day_from, day_to):
        print("The first date is not earlier than the second date")
        return False
    if not cpv_validation(cpv):
        return False
    return True
