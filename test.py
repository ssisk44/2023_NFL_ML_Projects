from models.objects.HistoryModel import HistoryModel
hM = HistoryModel("2016-08-01", "2023-10-24")
x = hM.calculateSeasonsInDateRange()
print(x)


















# counter = 0
# arr = []
# start = datetime.datetime.now()
# for a in range(0, 1000):
#     for b in range(0, 1000):
#         for c in range(0, 10):
#             # for d in range(0, 1000):
#                 # for e in range(0, 1000):
#             counter += 1
#             arr.append(101010010101010)
#             # arr.append([101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010, 101010010101010])
# end = datetime.datetime.now()
#
# print(counter)
# print(len(arr))
# print(end - start)


# generate combination integers

# generate lineups from combinations integers


# allLineups = {}
# allLineupsXD = []
# counter = 0
# try:
#     for qbIndex in range(0, len(qbArr)):
#         playerDataEntryQB = qbArr[qbIndex]
#         qbSalary = int(playerDataEntryQB[7])
#
#         qbIndexStr = str(qbIndex)
#         lineupPlayers = [playerDataEntryQB]
#         totalLineupSalary = qbSalary
#
#         for rbIndex in range(0, len(rbCombos)):
#             playerDataEntryRB1 = rbCombos[rbIndex][0]
#             playerDataEntryRB2 = rbCombos[rbIndex][1]
#
#             rbIndexStr = str(rbIndex)
#
#             lineupPlayers.append(playerDataEntryRB1)
#             totalLineupSalary += int(playerDataEntryRB1[7])
#
#             lineupPlayers.append(playerDataEntryRB2)
#             totalLineupSalary += int(playerDataEntryRB2[7])
#
#             for wrIndex in range(0, len(wrCombos)):
#                 playerDataEntryWR1 = wrCombos[wrIndex][0]
#                 playerDataEntryWR2 = wrCombos[wrIndex][1]
#                 playerDataEntryWR3 = wrCombos[wrIndex][2]
#
#                 wrIndexStr = str(wrIndex)
#
#                 lineupPlayers.append(playerDataEntryWR1)
#                 totalLineupSalary += int(playerDataEntryWR1[7])
#
#                 lineupPlayers.append(playerDataEntryWR2)
#                 totalLineupSalary += int(playerDataEntryWR2[7])
#
#                 lineupPlayers.append(playerDataEntryWR3)
#                 totalLineupSalary += int(playerDataEntryWR3[7])
#
#                 mapIndex = qbIndexStr + rbIndexStr + wrIndexStr
#                 allLineups[mapIndex] = lineupPlayers
#
#                 for teIndex in range(0, len(teArr)):
#                     playerDataEntryTE = teArr[teIndex]
#
#                     teIndexStr = str(teIndex)
#
#                     totalLineupSalary += int(playerDataEntryTE[7])
#                     if totalLineupSalary > 60000:
#                         continue
#                     lineupPlayers.append(playerDataEntryTE)
#
#                     mapIndex = qbIndexStr + rbIndexStr + wrIndexStr + teIndexStr
#                     allLineups[mapIndex] = lineupPlayers
#                     exit()
#
#
#
#                     for flxIndex in range(0, len(flxArr)):
#                         playerDataEntryFLX = flxArr[flxIndex]
#
#                         flxIndexStr = str(flxIndex)
#
#                         totalLineupSalary += int(playerDataEntryFLX[7])
#                         if totalLineupSalary > 60000:
#                             continue
#                         lineupPlayers.append(playerDataEntryFLX)
#
#                         for dIndex in range(0, len(dArr)):
#                             playerDataEntryD = flxArr[flxIndex]
#
#                             dIndexStr = str(dIndex)
#
#                             totalLineupSalary += int(playerDataEntryD[7])
#
#                             # if totalLineupSalary > 60000:
#                             #     continue
#
#                             # keepBool = getRandomNumberWithChance(wED)
#                             # if not keepBool:
#                             #     continue
#
#                             mapIndex = qbIndexStr + rbIndexStr + wrIndexStr + teIndexStr + flxIndexStr + dIndexStr
#                             print(mapIndex)
#                             exit()
#                             lineupPlayers.append(flxArr[flxIndex])
#                             allLineups[mapIndex] = lineupPlayers
#                             counter += 1
