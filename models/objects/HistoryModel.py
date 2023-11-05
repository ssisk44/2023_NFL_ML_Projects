import datetime
from models.objects.SeasonModel import SeasonModel
from src.func import dateStringToYearDayMonth
class HistoryModel:
    def __init__(self, dateRangeStart, dateRangeEnd):
        self.dateRangeStart = dateRangeStart
        self.dateRangeEnd = dateRangeEnd
        self.seasons = {}

    def calculateSeasonsInDateRange(self):
        startDateYear, startDateMonth, startDateDay = dateStringToYearDayMonth(self.dateRangeStart)

        endDateYear, endDateMonth, endDateDay = dateStringToYearDayMonth(self.dateRangeEnd)

        # any request past July will be considered as the following season
        startSeasonYear = startDateYear
        if startDateMonth > 7:
            startSeasonYear += 1

        endSeasonYear = endDateYear
        if endDateMonth > 7:
            endSeasonYear += 1

        return [startSeasonYear, endSeasonYear]



    def constructSeasons(self, seasonStartYear, seasonEndYear):
        for seasonYear in range(seasonStartYear, seasonEndYear):
            self.seasons[seasonYear] = SeasonModel(seasonYear, {"seasonFilterStartDate": self.dateRangeStart, "seasonFilterEndDate": self.dateRangeEnd})
