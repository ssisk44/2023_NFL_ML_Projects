import os
import pandas as pd
from Toolbox.utilityFunctions import getScheduleDataForRange
from Toolbox.Data_Processing import scheduleDataProcessor


def main():
    print('Attempting Schedule Data Processing')
    # try:
    scheduleDataProcessor.processScheduleData()
    # except Exception as e:
    #     print("Schedule Data Processing Failed")
    #     print(str(e))
    #     exit()
    print("Schedule Data Processing Complete!")

