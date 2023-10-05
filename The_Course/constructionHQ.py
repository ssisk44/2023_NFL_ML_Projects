from The_Toolbox.Data_Scrapping import scheduleScrapper as SS
import os

def main():
    # Obtain Schedule
    try:
        print("Beginning Schedule Scrapping")
        currentSeasonInt = int(os.environ.get("CURRENT_SEASON_YEAR"))
        SS.scrapeNFLScheduleForRange(2002, currentSeasonInt)
    except Exception:
        print("Schedule Scrapping Failed")
        exit()
    print("Schedule Scrapping Finished and Successful!")
