import logging


def dateStringToYearDayMonth(dateString: str):
    if len(dateString) != 10 or dateString[4] != '-' or dateString[7] != "-":
        logging.info("dateStringToYearMonthDay ERROR:" + dateString)
        exit()

    dateYear = int(dateString[0:4])
    dateMonth = int(dateString[5:7])
    dateDay = int(dateString[8:10])

    return dateYear, dateMonth, dateDay