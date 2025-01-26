from datetime import datetime
import re


def raw_date_stripping(date_str):
    try:
        # Replace mixed separators with a standard one
        date_str = re.sub(r'[.\-]', '.', date_str)
        day, month, year = map(int, date_str.split('.'))
        # Validate date using datetime
        datetime(year, month, day)
        return day, month, year
    except ValueError:
        print(f"{date_str} is an invalid date")
        return False


def is_first_date_lesser(raw_first_date, raw_second_date):
    date_format = "%Y-%m-%d"
    first_date_couple = raw_date_stripping(raw_first_date)
    second_date_couple = raw_date_stripping(raw_second_date)
    if not first_date_couple or not second_date_couple:
        print("Error with date stripping")
        return None  # Invalid input dates

    date1 = f"{first_date_couple[2]}-{first_date_couple[1]:02}-{first_date_couple[0]:02}"
    date2 = f"{second_date_couple[2]}-{second_date_couple[1]:02}-{second_date_couple[0]:02}"
    try:
        # Parse the input strings into datetime objects
        first_date = datetime.strptime(date1, date_format)
        second_date = datetime.strptime(date2, date_format)

        # Compare the dates
        return first_date < second_date
    except ValueError as e:
        print(f"Error: {e}")
        return None


def date_validation(first_date, second_date):
    return bool(raw_date_stripping(first_date) and raw_date_stripping(second_date))


def cpv_validation(cpv_code):
    if not cpv_code:
        print("Please enter the CPV code")
        return False
    elif re.fullmatch(r"\d{8}-\d", cpv_code):  # Strict match
        return True
    else:
        print(f'"{cpv_code}" is not a valid CPV code.\n'
              f'A valid CPV code should consist of 8 digits, a dash, and 1 digit (e.g., 42111100-1).')
        return False


def validations(day_from, day_to, cpv):
    if not date_validation(day_from, day_to):
        print("One or both dates are invalid")
        return False
    if not is_first_date_lesser(day_from, day_to):
        print("The first date is not earlier than the second date")
        return False
    if not cpv_validation(cpv):
        return False
    return True

