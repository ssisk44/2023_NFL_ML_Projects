# qbSalaryRange = [5200, 8200]
# rbSalaryRange = [4500, 9300]
# wrSalaryRange = [4000, 9300]
# teSalaryRange = [3100, 6400]
# flxSalaryRange = [3100, 9300]
# dSalaryRange = [2200, 4100]
#
# # number of combinations
# qbNum = int((qbSalaryRange[1]-qbSalaryRange[0])/100)
# rb1Num = int((rbSalaryRange[1]-rbSalaryRange[0])/100)
# rb2Num = int((rbSalaryRange[1]-rbSalaryRange[0])/100)
# wr1Num = int((wrSalaryRange[1]-wrSalaryRange[0])/100)
# wr2Num = int((wrSalaryRange[1]-wrSalaryRange[0])/100)
# wr3Num = int((wrSalaryRange[1]-wrSalaryRange[0])/100)
# teNum = int((teSalaryRange[1]-teSalaryRange[0])/100)
# flxNum = int((flxSalaryRange[1]-flxSalaryRange[0])/100)
# dNum = int((dSalaryRange[1]-dSalaryRange[0])/100)
#
# print(qbNum, rb1Num, rb2Num, wr1Num, wr2Num, wr3Num, teNum, flxNum, dNum)
#
# print(qbNum*rb1Num*rb2Num*wr1Num*wr2Num*wr3Num*teNum*flxNum*dNum)
#
#
# for qbSalary in range(qbSalaryRange[0], qbSalaryRange[1], 100):
#     for rbSalary1 in range(rbSalaryRange[0], rbSalaryRange[1], 100):
#         for rbSalary2 in range(rbSalaryRange[0], rbSalaryRange[1], 100):
#             for wrSalary1 in range(wrSalaryRange[0], wrSalaryRange[1], 100):
#                 for wrSalary2 in range(wrSalaryRange[0], wrSalaryRange[1], 100):
#                     for wrSalary3 in range(wrSalaryRange[0], wrSalaryRange[1], 100):
#

mockLineupSalaryArr = [8300, 6300, 4800, 5200, 3900, 4500, 8000, 4700, 3300]

def determineRequiredPointsForLineupEntryPositionSalary(lineupSalaryArr, targetPoints=238.06, lineupTotalSalary=50000):
    """
    This function is meant to understand the proportionate points value of each player in a contest entry from salary
    :param lineupSalaryArr:
    :param targetPoints:
    :param lineupTotalSalary: this will always be 50000 because you have to compare it to the maximum for all entries
    :return:
    """
    retArr = []
    for p_salary in lineupSalaryArr:
        retArr.append(round(p_salary*targetPoints/lineupTotalSalary, 2))
    return retArr

def determineRequiredPlayerPointsForSalary(playerSalary, playerAvgPts):


xd = determineRequiredPointsForLineupEntryPositionSalary(mockLineupSalaryArr)
print(xd, sum(mockLineupSalaryArr))