from src.functions.data.dfs.bdb import historicalDFSDataFuncs

"""
This file is responsible for two things:
1) Generating 

"""





### Create require player output per salary, output efficiency, and point-efficiency metric
# obtain historicalDFSPlayerResults DFS data for each week and year
dfsHistoricalDF = historicalDFSDataFuncs.getDFSHistoricalRecordsForSeasonWeek(2023, 11)


dfsHistoricalDF = historicalDFSDataFuncs.filterDFSHistoricalRecords(dfsHistoricalDF)

# filter out non-main slate games

# manual filtration step -> remove players who haven't scored over 10 points in a week this year?

# separate players into positional categories

# find total combinations number

#

