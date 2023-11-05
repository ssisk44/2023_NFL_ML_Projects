from src.dataAnalysis.scheduleDataAnalysis import predictScheduleDataOutcomes

def main():
    print('Attempting Schedule Data Analysis')
    # try:
    predictScheduleDataOutcomes("SGOSD_V1.py", "2023-10-10", "2023-10-20")
    # except Exception as e:
    #     print("Schedule Data Analysis Failed")
    #     print(str(e))
    #     exit()
    print("Schedule Data Analysis Complete!")
