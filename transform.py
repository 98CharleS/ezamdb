import pandas as pd
from datetime import datetime

tenders = []

formats = [
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d"
]


def appending_deals(database, id_n=1):
    # id_n for numering tenders
    # changing raw data to json type
    if database:
        database = database.json()

        def getting_deals(x):  # script to return valves from the deal obj
            publication_time = deal.get("publicationDate")

            # Parse the timestamp
            for fmt in formats:
                try:
                    dt = datetime.strptime(publication_time.rstrip("Z"), fmt)
                    break
                except ValueError:
                    dt = None

            if dt is None:
                print(f"Unrecognized date format: {publication_time}")
                return None

            # Extract date and time
            publication_date = dt.strftime("%Y-%m-%d")
            publication_hour = dt.strftime("%H:%M:%S")

            return {
                "id": x,
                "ObjectId": deal.get("objectId"),
                "orderObject": deal.get("orderObject"),
                "orderType": deal.get("orderType"),
                "publicationDate": publication_date,
                "publicationHour": publication_hour,
                "Result": deal.get("procedureResult"),
            }

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
