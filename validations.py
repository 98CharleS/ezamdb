from datetime import datetime
import re


def raw_date_stripping(date_str):
    date_pattern = r'^(\d{1,2})[.\-](\d{1,2})[.\-](\d{4})$'

    match = re.match(date_pattern, date_str)
    if match:
        day, month, year = map(int, match.groups())
        # Validate the day and month ranges
        if 1 <= day <= 31 and 1 <= month <= 12:
            return day, month, year
    else:
        print(f"{date_str} is wrong date")
        return False


def is_first_date_lesser(raw_first_date, raw_second_date):
    date_format = "%Y-%m-%d"
    first_date_couple = raw_date_stripping(raw_first_date)
    second_date_couple = raw_date_stripping(raw_second_date)
    date1 = f"{first_date_couple[2]}-{first_date_couple[1]}-{first_date_couple[0]}"
    date2 = f"{second_date_couple[2]}-{second_date_couple[1]}-{second_date_couple[0]}"
    print(date1, date2)
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

    if raw_date_stripping(first_date) and raw_date_stripping(second_date):
        return True
    else:
        return False


def cpv_validation(cpv_code):
    if not cpv_code:
        # if empty
        print("Please enter the link code")
        return False
    elif re.search("[0-9]{8}-[0-9]", cpv_code): # checking if link has correct structure
        return True
    else:
        print(f'"{cpv_code}" is not valid CPV code\n CPV code should be made of 8 digits, dash and 1 digit\n'
                  f'Like this: 42111100-1')
        return False


def validations(day_from, day_to, cpv):
    if date_validation(day_from, day_to):
        if is_first_date_lesser(day_from, day_to):
            if cpv_validation(cpv):
                return True
    else:
        return False
