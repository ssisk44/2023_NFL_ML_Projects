from bs4 import BeautifulSoup
import requests
import pandas as pd
import time, os
from Toolbox.teamNaming import teamNameToSportsReferenceAbbreviationMap

def scrapeNFLGameMetadata():
    # TODO: attempt to only scrape metadata for games not already in data, or at least for only the current year
    scheduleDataDir = "Data/Schedules/"
    scheduleDataDirFileList = os.listdir(scheduleDataDir)
    for file in scheduleDataDirFileList:
        seasonGamesArr = pd.read_csv(scheduleDataDir + file).to_numpy()

        """
        For each game in a season get the following information
        1) Year - seasonGamesArr
        2) Week - seasonGamesArr
        3) Date - seasonGamesArr
        4) Time - seasonGamesArr
        5) Place - seasonGamesArr
        6) Away Team - seasonGamesArr
        7) Home Team - seasonGamesArr
        8) Away Team Score - seasonGamesArr
        9) Home Team Score - seasonGamesArr
        10) Away Team Season Win % - needs calculation
        11) Home Team Season Win % - needs calculation
        12) Away Team Coach - scrapping
        13) Home Team Coach - scrapping
        14) Coin Toss Winner - scrapping
        15) Roof - scrapping
        16) Surface - scrapping
        17) Duration - scrapping
        18) Attendance - scrapping
        19) Weather Temperature - scrapping
        20) Weather Descriptor - scrapping
        20) Line - scrapping
        21) O/U - scrapping
        22) Away Team Rest Days - calculation
        23) Home Team Rest Days - calculation
        24) Away Team Travel Distance - calculation
        25) Home Team Travel Distance - calculation
        26) Away Team Consecutive Away Games - calculation
        """

        # for entry in seasonGamesArr:
        #     year = entry[0]
        #     day = entry[1]
        #     date = entry[2]
        #
        #     html = requests.get(gameLink).content
        #     soup = BeautifulSoup(html, "html.parser")
        #     print(soup)
        #     df_list = pd.read_html(html)
        #     print(gameLink)

        exit()
