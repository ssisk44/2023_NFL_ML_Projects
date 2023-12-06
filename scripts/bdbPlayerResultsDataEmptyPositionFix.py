import os
import dotenv
import pandas as pd
import math
from src.constants import bdbColumns

""" replace all empty DK positions with FD positions """
dotenv.load_dotenv()
absProjectPath = os.getenv("ABS_PROJECT_PATH")
apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
apiDataYearEnd = int(os.getenv("CURRENT_SEASON_YEAR"))
for year in range(apiDataYearStart, apiDataYearEnd+1):
    df = pd.read_csv(absProjectPath + 'data/dfs/historicalDFSPlayerResults/csv/' + str(year) + '.csv', index_col=None)
    rowArr = []
    for i,row in df.iterrows():
        dkPosition = row['DK Position']
        fdPosition = str(row['FD Position'])
        if str(dkPosition) == "nan":
            if str(fdPosition) == "D":
                fdPosition = "DST"
            row['DK Position'] = fdPosition
        rowArr.append(row)
    pd.DataFrame(rowArr, columns=bdbColumns).to_csv(absProjectPath + "data/dfs/historicalDFSPlayerResults/csv/" + str(year) + ".csv", index=False)
