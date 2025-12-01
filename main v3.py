import pandas as pd
from validations import validations
from extract import extract
from db_transform import appending_deals
from date_transform import transforming_to_datetime
from datetime import datetime

# GUI
# taking dates and cpv
# formatting it for
# making link
# getting data
# formatting data


def making_link(day_from: datetime, day_to: datetime, cpv, last_id=None):
    # Format datetimes directly into the API format
    starting = day_from.strftime("%Y-%m-%dT00:00:00")
    ending = day_to.strftime("%Y-%m-%dT23:59:59")
    # cpv is code which specify a kind of work to be made in deal

    # adding next page of database if needed
    if last_id is None:
        search_after_addition = ""
    else:
        search_after_addition = f"&SearchAfter={last_id}"

    # link to access eZam API
    if cpv != "all":
        # CPV without specification so database have to return all of CPVs
        link = ("https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&CpvCode="
                + cpv + "&PublicationDateFrom="
                + starting + "&PublicationDateTo="
                + ending + "&PageSize=500"
                + search_after_addition)
        return link
    else:
        link = ("https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&"
                + "&PublicationDateFrom="
                + starting + "&PublicationDateTo="
                + ending + "&PageSize=500")
        return link


def taking_data():
    sday = input("Enter the starting day of range:\n")
    lday = input("Enter the ending day of range:\n")
    cpvs = input("Enter the CPV code. If many separate them using ','. "
                 "If you are interested in all tenders type 'all':\n")
    return sday, lday, cpvs


date1 = "01.01.2023"  # for future adjustment make it entered by user
date2 = "02.05.2023"
cpv = "44212200-1" # 44212200-1 / all


def main(start_day_str, end_day_str, code):
    # first_day, second_day, cpv_code = taking_data() # will be used in future to take user input
    # checking if input is in correct forms
    if validations(start_day_str, end_day_str, code):
        print("validation passed")
        # converting string dates from input to datetime formats
        start_date = transforming_to_datetime(start_day_str)
        end_date = transforming_to_datetime(end_day_str)

        db = []

        # first run:
        print(start_date, end_date, code)
        link = making_link(start_date, end_date, code)
        print(link)
        db = appending_deals(extract(link))

        # dodging empty db
        if db:
            # Create a DataFrame
            df = pd.DataFrame(db)
            # Convert publicationDate to datetime
            df['publicationDate'] = pd.to_datetime(df['publicationDate'])
            df.to_csv('output.csv', index=False, sep=";") # in Europe here so ";" instead of ","
            last_obj_id = df['ObjectId'].iloc[-1]
            last_num = df['id'].iloc[-1]
            print(last_obj_id, last_num)

            # LOOP TO DO

            """while db:
                link = making_link(start_date, end_date, code, last_obj_id)
                db = appending_deals(extract(link))
                # Create a DataFrame
                df = pd.DataFrame(db)
                # Convert publicationDate to datetime
                df['publicationDate'] = pd.to_datetime(df['publicationDate'])
                df.to_csv('output.csv', index=False, sep=";")  # in Europe here so ";" instead of ","
                last_obj_id = df['ObjectId'].iloc[-1]
                last_num = df['id'].iloc[-1]"""
        else:
            print("db empty at first run")
    else:
        print("Error at validation stage")


if __name__ == '__main__':
    main(date1, date2, cpv)

