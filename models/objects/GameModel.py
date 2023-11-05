from models.objects.FranchiseModel import FranchiseModel
class GameModel:
    def __init__(self, seasonYear, seasonWeek, awayFranchiseInt, homeFranchiseInt):
        self.seasonYear = seasonYear
        self.seasonWeek = seasonWeek

        self.awayFranchiseInt = awayFranchiseInt
        self.awayFranchise = FranchiseModel(self.awayFranchiseInt)

        self.homeFranchiseInt = homeFranchiseInt
        self.homeFranchise = FranchiseModel(self.homeFranchiseInt)

        self.gameID = str(seasonYear) + "-" + str(seasonWeek) + "-" + str(awayFranchiseInt) + "-" + str(homeFranchiseInt)



    def construct(self):
        None


