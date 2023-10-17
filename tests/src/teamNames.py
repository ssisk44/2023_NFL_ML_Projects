import unittest
import os
from src import teamNaming


class CaseControllerTest(unittest.TestCase):
    def testGetAllTeamNamesBySeason(self):
        testYears = [2002, 2016, 2017, 2019, 2020, 2021, 2023]
        testYearsTeamNames = []

        os.environ["CURRENT_SEASON_YEAR"] = "2023"
        teamNaming.getAllTeamNamesForEverySeason()

    def testGetCurrentTeamNameForFranchise(self):
        res1 = teamNaming.getCurrentTeamNameForFranchise("Washington Football Team")
        res2 = teamNaming.getCurrentTeamNameForFranchise("Washington Commanders")
        self.assertEqual(res1, res2)
        self.assertEqual("Washington Commanders", res1)


if __name__ == '__main__':
    unittest.main()
