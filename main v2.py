import pandas as pd
from validations import validations
from link_maker import making_link
from extract import extract
from db_transform import appending_deals
from date_transform import transforming_to_datetime
from datetime import timedelta

# GUI
# taking dates and cpv
# formatting it for
# making link
# getting data
# formatting data


def taking_data():
    sday = input("Enter the starting day of range:\n")
    lday = input("Enter the ending day of range:\n")
    cpvs = input("Enter the CPV code. If many separate them using ','. "
                 "If you are interested in all tenders type 'all':\n")
    return sday, lday, cpvs


dates = []

date1 = "15.01-2023"  # for future adjustment make it entered by user
date2 = "15-01.2025"
cpv = "all"


# TEST WITH SAME DATE
def engine(d1, d2, code):
    link = making_link(d1, d2, code)
    print(link)
    db = appending_deals(extract(link))
    print(db)
    # Create a DataFrame
    df = pd.DataFrame(db)

    # Convert publicationDate to datetime
    df['publicationDate'] = pd.to_datetime(df['publicationDate'])
    df.to_csv('output.csv', index=False)


def main(start_day_str, end_day_str, code):
    # first_day, second_day, cpv_code = taking_data()
    if validations(start_day_str, end_day_str, code):
        print("validation passed")
        link = making_link(start_day_str, end_day_str, code)
        print(link)
        db = []
        start_date = transforming_to_datetime(start_day_str)
        end_date = transforming_to_datetime(end_day_str)
        first_day_in_range = start_date
        second_day_in_range = first_day_in_range + timedelta(days=1)
        while second_day_in_range <= end_date: # looping through all dates from dates range
            print(first_day_in_range, second_day_in_range)
            db = appending_deals(extract(link)) # HERE IT IS NEEDED TO MAKE PROGRAM ADD MORE DATA FOR DB THEN CLOSE AND PROCEED TO NEXT POINT
        # Create a DataFrame
        df = pd.DataFrame(db)
        # Convert publicationDate to datetime
        df['publicationDate'] = pd.to_datetime(df['publicationDate'])
        df.to_csv('output.csv', index=False)
    else:
        print("Error at validation stage")


if __name__ == '__main__':
    main(date1, date2, cpv)







"""    BACKUP COPY
def main(start_day, end_day, code):
    # first_day, second_day, cpv_code = taking_data()
    if validations(start_day, end_day, code):
        looping_for_days(start_day, end_day, engine(start_day, end_day, code))
        link = making_link(start_day, end_day, code)
        print(link)
        db = appending_deals(extract(link))
        print(db)
        # Create a DataFrame
        df = pd.DataFrame(db)
        # Convert publicationDate to datetime
        df['publicationDate'] = pd.to_datetime(df['publicationDate'])
        df.to_csv('output.csv', index=False)
    else:
        print("Error at main")
"""