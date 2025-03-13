import pandas as pd
from datetime import datetime

tenders = []


def appending_deals(database):
    # changing raw data to json type
    if database:
        database = database.json()

        def getting_deals(x):  # script to return valves from the deal obj
            publication_time = deal.get("publicationDate")

            # Parse the timestamp
            dt = datetime.strptime(publication_time[:-1], "%Y-%m-%dT%H:%M:%S.%f")

            # Extract date and time
            publication_date = dt.strftime("%Y-%m-%d")
            publication_hour = dt.strftime("%H:%M:%S")

            return {
                "id": x,
                "orderObject": deal.get("orderObject"),
                "orderType": deal.get("orderType"),
                "publicationDate": publication_date,
                "publicationHour": publication_hour,
                "Result": deal.get("procedureResult"),
            }

        id_n = 1  # number for numering tenders

        for deal in database:  # making a list of deals then return info
            tenders.append(getting_deals(id_n))
            id_n = id_n + 1
        return tenders
    else:
        print("Error at appending tenders")


def pandas(raw_db):
    # converting database to pandas
    df = pd.DataFrame(raw_db)
    # spitting publicationTime into hour and date
    df['publicationDate'] = pd.to_datetime(df['publicationDate'])
    print(df.head())
