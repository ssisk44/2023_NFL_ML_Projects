import os
from src.data.playerIDBridgeFuncs import getAllHistoricalWeeklyPlayerData

""" The purpose of this routine is to collect DK Player ID to API Stats to historical results data to bridge the player identification issue"""




### Read and compile historical results from 2017-2023, filter by contest positions, sort by first name, attach to historical and DK
apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
apiDataYearEnd = int(os.getenv("CURRENT_SEASON_YEAR"))
allAPIPlayerData = getAllHistoricalWeeklyPlayerData(apiDataYearStart, apiDataYearEnd+1)


### Read in DK contest csv, sort by first name, attach to historical
