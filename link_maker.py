from datetime import datetime


def making_link(day_from: datetime, day_to: datetime, cpv, last_id=None):
    # format datetimes directly into the API format
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
