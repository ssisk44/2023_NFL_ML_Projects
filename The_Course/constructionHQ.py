from The_Toolbox.Data_Scrapping import scheduleScrapper as SS
import os

def main():
    print("Beginning Schedule Scrapping")
    currentSeasonInt = int(os.environ.get("CURRENT_SEASON_YEAR"))
    SS.getNFLScheduleForRange(2002, currentSeasonInt)