def breaking_date(date_str):
    d, m, y = date_str.replace("-", ".").split(".")
    return d, m, y


def making_link(day_from, day_to, cpv):

    # converting today time to format used in eZam service
    df_y, df_m, df_d = breaking_date(day_from)

    # converting time a week ago to format used in eZam service
    dt_y, dt_m, dt_d = breaking_date(day_to)

    starting = df_y + "-" + df_m + "-" + df_d + "T00:00:00"
    ending = dt_y + "-" + dt_m + "-" + dt_d + "T23:59:59"
    # cpv is code which specify a kind of work to be made in deal

    # link to access eZam API
    link = ("https://ezamowienia.gov.pl/mo-board/api/v1/notice?NoticeType=ContractNotice&TenderType=1.1.1&CpvCode=" +
            cpv + "&PublicationDateFrom=" + starting + "&PublicationDateTo=" + ending + "&PageSize=100")
    return link
