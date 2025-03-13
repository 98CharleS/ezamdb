import pandas as pd
from validations import validations
from link_maker import making_link
from extract import extract
from transform import appending_deals

# GUI
# taking dates and cpv
# formatting it for
# making link
# getting data
# formatting data


def taking_data():
    sday = input("Enter the starting day of range:\n")
    lday = input("Enter the ending day of range:\n")
    cpvs = input("Enter the CPV code. If many separate them using ',':\n")

    return sday, lday, cpvs


dates = []

date1 = "15.01-2015"  # for future adjustment make it entered by user
date2 = "15.01.2025"
cpv = "45000000-7"


def main():
    # first_day, second_day, cpv_code = taking_data()
    if validations(date1, date2, cpv):
        link = making_link(date1, date2, cpv)
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


main()
