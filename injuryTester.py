import pandas as pd
import json
import os
import dotenv

dotenv.load_dotenv()
f = open(os.getenv('ABS_PROJECT_PATH') + '/data/msf/injury_history.csv')
x = json.load(f)

player_data_dict = x[0]['player']
print("Injury History Player: ", x[0]['player'])

player_injury_history_dict = x[0]['injuryHistory']
print("Injury History Length: ", len(player_injury_history_dict[0]))

entryCounter = 0
for entry in player_injury_history_dict:
    print("Entry Number " + str(entryCounter) + ": " + str(entry))
    entryCounter += 1