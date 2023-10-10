import team as Team

class Game:
    def __init__(self, week, day: str, time: str, homeTeam: Team, awayTeam: Team):
        self.week = week
        self.day = day
        self.time = time
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
