import player as Player


class Team:
    def __init__(self, teamName: str, teamAbbreviation: str, franchiseNum: int, players: list):
        self.teamName = teamName
        self.teamAbbreviation = teamAbbreviation
        self.franchiseNum = franchiseNum
        self.players = [Player]
