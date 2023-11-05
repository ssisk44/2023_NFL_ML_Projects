from src import constants as Constant

class FranchiseModel:
    def __init__(self, teamInt:int):
        self.franchiseTeamInt = teamInt
        self.franchiseCurrentTeamName = None
        self.franchiseAbbreviation = Constant.teamNameToTeamAbbreviationMap[self.franchiseTeamInt]



