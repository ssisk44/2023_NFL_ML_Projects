import logging
import os

### this file needs to be forming a trainingmodelschema for each request dataTypes then run class functions on it in
def completeRequest(args: list):
    dataTypes = args[0]

    # train models on latest data
    if "Schedule" in dataTypes:
        logging.info("Beginning Training On Newest Data")
        trainSingleGameModelScheduleData()


def trainSingleGameModelScheduleData():
    try:
        logging.info("Beginning Schedule Data Scrapping")
        scheduleV1.trainScheduleModel()
    except Exception as e:
        logging.error("Schedule Scrapping FAILED", e)
        exit()
    logging.info("Scrapped Schedule Data Successful!")

