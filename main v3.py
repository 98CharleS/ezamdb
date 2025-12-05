import pandas as pd
from validations import validations
from extract import extract
from date_transform import transforming_to_datetime
from datetime import datetime

# GUI
# taking dates and cpv
# formatting it for
# making link
# getting data
# formatting data


def making_dataframe(dataframe):
    try:
        x = pd.DataFrame(dataframe)
        return x
    except ValueError:
        return None


tenders = []


def appending_deals(database, id_n=1):
    # id_n for numering tenders
    # changing raw data to json type
    if database:
        database = database.json()

        def getting_deals(x):  # script to return valves from the deal obj

            return {
                "id": x,
                "ObjectId": deal.get("objectId"),
                "tenderId": deal.get("tenderId"),
                "noticeNumber": deal.get("noticeNumber"),
                "bzpNumber": deal.get("bzpNumber"),
                "orderObject": deal.get("orderObject"),
                "orderType": deal.get("orderType"),
                "cpvCode": deal.get("cpvCode"),
                "publicationDate": deal.get("publicationDate"),
                "submittingOffersDate": deal.get("submittingOffersDate"),
                "organizationName": deal.get("organizationName"),
                "organizationCity": deal.get("organizationCity"),
                "organizationCountry": deal.get("organizationCountry"),
                "isBelowEUThreshold": deal.get("isTenderAmountBelowEU"),
                "Result": deal.get("procedureResult")
            }

        for deal in database:  # making a list of deals then return info
            tenders.append(getting_deals(id_n))
            id_n = id_n + 1
        return tenders
    else:
        print("Error at appending tenders")


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
                + ending + "&PageSize=500"
                + search_after_addition)
        return link


def taking_data():
    sday = input("Enter the starting day of range:\n")
    lday = input("Enter the ending day of range:\n")
    cpvs = input("Enter the CPV code. If many separate them using ','. "
                 "If you are interested in all tenders type 'all':\n")
    return sday, lday, cpvs


date1 = "01.01.2023"  # for future adjustment make it entered by user
date2 = "01.01.2025"
cpv = "all"  # 44212200-1 / all


def main(start_day_str, end_day_str, code):
    # first_day, second_day, cpv_code = taking_data() # will be used in future to take user input
    # checking if input is in correct forms
    if validations(start_day_str, end_day_str, code):
        print("validation passed")
        # converting string dates from input to datetime formats
        start_date = transforming_to_datetime(start_day_str)
        end_date = transforming_to_datetime(end_day_str)

        # first run:
        print("first connection")
        print(start_date, end_date, code)  # printing input config
        link = making_link(start_date, end_date, code)  # making link to connect DB
        print(link)
        db = appending_deals(extract(link))  # extracting data from eZam DB and appending it into list

        # dodging empty db
        if db:
            print("first df")
            # Create a DataFrame
            df = making_dataframe(db)  # creating dataframe with pandas to read data from web

            # picking last num from downloaded data and last id of tender to get next page of data from this tender
            last_obj_id = df['ObjectId'].iloc[-1]
            last_num = df['id'].iloc[-1]
            print(last_obj_id, last_num)
            print("entering loop")
            repeat = 0
            while True:
                # loop which will go on as long as downloaded list of data is not empty
                # used to get all pages form eZam DB
                repeat = repeat + 1
                print(f"loop #{repeat}")

                # making link to connect to eZam BD and download data after last_obj_id
                link = making_link(start_date, end_date, code, last_obj_id)
                print(link)

                # extracting data from eZam DB and appending it into list
                db = appending_deals(extract(link), last_num + 1)

                print("next df")
                # Create a DataFrame
                df = making_dataframe(db)  # creating dataframe with pandas to read data from web

                # picking last num from downloaded data and last id of tender to get next page of data from this tender
                new_last_obj_id = df['ObjectId'].iloc[-1]
                new_last_num = df['id'].iloc[-1]

                if new_last_num == last_num:
                    print("ending loop")
                    break
                else:
                    last_num = new_last_num
                    last_obj_id = new_last_obj_id
                    print(last_obj_id, last_num)


                """if db:
                    df = making_dataframe(db)
                    # Convert publicationDate to datetime
                    df['publicationDate'] = pd.to_datetime(df['publicationDate'])
                    df.to_csv('output.csv', index=False, sep=";")  # in Europe here so ";" instead of ","
                    last_obj_id = df['ObjectId'].iloc[-1]
                    last_num = df['id'].iloc[-1]
                    print(last_obj_id, last_num)
                else:
                    print("breaking loop")
                    break"""

            """# Convert publicationDate from eZam DB to datetime
            df['publicationDate'] = pd.to_datetime(df['publicationDate'])"""
            # Exporting dataframe to csv file
            df.to_csv('output.csv', index=False, sep=";")  # in Europe here so ";" instead of ","
        else:
            print("db empty at first run")
    else:
        print("Error at validation stage")
    print("that's all")



if __name__ == '__main__':
    main(date1, date2, cpv)
