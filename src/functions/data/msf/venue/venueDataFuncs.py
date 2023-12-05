import pandas as pd
import os
import dotenv

def getVenueEntryByID(venueID:int):
    dotenv.load_dotenv()
    df = pd.read_csv(str(os.getenv("ABS_PROJECT_PATH")) + "data/msf/all_venues.csv", index_col=False)
    df = df.loc[df['Venue ID'] == venueID]
    print(df)
    return df

getVenueEntryByID(196)



