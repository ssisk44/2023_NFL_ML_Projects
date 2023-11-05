import logging
class SeasonModel:
    def __init__(self, seasonYear:int, args: dict):
        self.games = {}
        self.seasonYear = seasonYear
        self.args = args

    def construct(self):
        self.createGamesForSeason()

    def createGamesForSeason(self):
        # ensure date range has been passed to filter games
        if "seasonFilterStartDate" not in self.args.keys():
            logging.info("SeasonModel args did not contain 'seasonFilterStartDate'")
        if "seasonFilterEndDate" not in self.args.keys():
            logging.info("SeasonModel args did not contain 'seasonFilterEndDate'")

        filterStartDate = self.args["seasonFilterStartDate"]
        filterEndDate = self.args["seasonFilterStartDate"]



