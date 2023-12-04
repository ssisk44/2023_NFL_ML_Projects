import logging
import os
import dotenv
import pandas as pd


def dateStringToYearDayMonth(dateString: str):
    if len(dateString) != 10 or dateString[4] != '-' or dateString[7] != "-":
        logging.info("dateStringToYearMonthDay ERROR:" + dateString)
        exit()

    dateYear = int(dateString[0:4])
    dateMonth = int(dateString[5:7])
    dateDay = int(dateString[8:10])

    return dateYear, dateMonth, dateDay

def calculateSeasonYearFromDate(date: str):
    year = int(date[:4])
    month = int(date[5:7])

    # games before May are all considered in the previous season year
    if month <= 4:
        year -= 1

    return year

