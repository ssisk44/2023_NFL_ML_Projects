from src.dataManipulation import scheduleDataManipulator


def main():
    print(' Attempting Schedule Data Processing')
    # try:
    scheduleDataManipulator.processScheduleData()
    # except Exception as e:
    #     print("Schedule data Processing Failed")
    #     print(str(e))
    #     exit()
    print(" Schedule data Processing Complete!")

