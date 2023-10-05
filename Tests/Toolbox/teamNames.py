import unittest
import os
from The_Toolbox import teamNames


class CaseControllerTest(unittest.TestCase):
    def testGetAllTeamNamesBySeason(self):
        testYears = [2002, 2016, 2017, 2019, 2020, 2021, 2023]
        testYearsTeamNames = []

        os.environ["CURRENT_SEASON_YEAR"] = "2023"
        teamNames.getAllTeamNamesForEverySeason()

    def testGetCurrentTeamNameForFranchise(self):
        res1 = teamNames.getCurrentTeamNameForFranchise("Washington Football Team")
        res2 = teamNames.getCurrentTeamNameForFranchise("Washington Commanders")
        self.assertEqual(res1, res2)
        self.assertEqual("Washington Commanders", res1)


if __name__ == '__main__':
    unittest.main()
