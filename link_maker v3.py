from datetime import datetime


def breaking_date(date_str):
    d, m, y = date_str.replace("-", ".").split(".")
    return d, m, y


def making_link(day_from: datetime, day_to: datetime, cpv):
    # Format datetimes directly into the API format
    starting = day_from.strftime("%Y-%m-%dT00:00:00")
    ending = day_to.strftime("%Y-%m-%dT23:59:59")
    # cpv is code which specify a kind of work to be made in deal

    # link to access eZam API
    if cpv != "all":
        link = ("https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&CpvCode="
                + cpv + "&PublicationDateFrom=" + starting + "&PublicationDateTo=" + ending + "&PageSize=500")
        return link
    else:
        link = ("https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&"
                + "&PublicationDateFrom=" + starting + "&PublicationDateTo=" + ending + "&PageSize=500")
        return link


def fetch_all_pages(starting, ending, code):
    page = 1
    all_results = []

    while True:
        link = (
            "https://ezamowienia.gov.pl/mo-board/api/v1/notice?"
            "NoticeType=ContractNotice&TenderType=1.1.1&"
            f"PublicationDateFrom={starting}&PublicationDateTo={ending}&"
            f"PageSize=500&PageNumber={page}"
        )

        data = extract(link)  # your function
        if not data:          # empty list → no more pages
            break

        all_results.extend(data)
        page += 1

    return all_results