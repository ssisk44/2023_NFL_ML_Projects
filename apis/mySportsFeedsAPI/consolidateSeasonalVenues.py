import os
import dotenv
import pandas as pd


def consolidateUniqueVenues():
    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/nfl/seasonal_venues/"
    fullTargetDirPath = absProjectPath + targetDirectory

    venueDFArr = []
    for filename in os.listdir(fullTargetDirPath):
        filepath = fullTargetDirPath + filename
        df = pd.read_csv(filepath, index_col=False)
        venueDFArr.append(df)

    df = pd.concat(venueDFArr).drop_duplicates(subset=["Venue ID"])
    pd.DataFrame(df).to_csv(absProjectPath + 'data/nfl/all_venues.csv', index=False)


