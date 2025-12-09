import requests

tenders = []


def appending_deals(database, id_n=1):
    # changing raw data to json type
    # id_n for numering tenders

    if database:
        database = database.json()

        def getting_deals(x):  # script to return valves from the tender

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

        for deal in database:  # going through all tenders in list
            tenders.append(getting_deals(id_n))
            id_n = id_n + 1
        return tenders
    else:
        print("Error at appending tenders")


def extract(link):
        try:  # checking if eZam is available
            data = requests.get(link, timeout=10)
            data.raise_for_status()
            return data
        except requests.exceptions.Timeout:
            print("Network error.\nConnection to eZam timeout")
        except requests.exceptions.RequestException as error:
            print(f"{error} error")
