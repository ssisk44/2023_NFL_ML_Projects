from analysis.Single_Game_Outcome_Schedule_Data.versions import SGOSD_V1


def main():
    print('Attempting Schedule Data Analysis')
    # try:
    SGOSD_V1.main()
    # except Exception as e:
    #     print("Schedule Data Analysis Failed")
    #     print(str(e))
    #     exit()
    print("Schedule Data Analysis Complete!")
