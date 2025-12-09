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


def transforming_to_datetime(raw_date):
    date_format = "%Y-%m-%d"
    date_couple = raw_date_stripping(raw_date)
    if not raw_date:
        print("Error with date stripping")
        return None  # Invalid input date

    new_date = f"{date_couple[2]}-{date_couple[1]:02}-{date_couple[0]:02}"
    try:
        # Parse the input strings into datetime objects
        new_date = datetime.strptime(new_date, date_format)

        # returning date in right format
        return new_date
    except ValueError as e:
        print(f"Error encounter while transforming {raw_date}: {e}")
        return None
