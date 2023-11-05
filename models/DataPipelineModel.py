import os
import logging
from src.dataPipeline.dataTransformers import scheduleDataTransformer
from src.dataPipeline.dataScrappers import scheduleDataScrapper
from src.dataPipeline.dataScrappers import gameDataScrapper

class DataPipeline:
    def __init__(self, requestType, dataTypes, actionType):
        self.requestType = requestType
        self.dataTypes = dataTypes
        self.actionType = actionType

    def handlePipelineRequest(self):
        # Case 1: initializing a local dataset (ONE TIME PER NEW SYSTEM)
        if self.actionType == "I":
            logging.info("Initializing Local Data Through Pipeline")
            if "Schedule" in self.dataTypes:
                self.scheduleDataInitialization()

            if "Game/Player" in self.dataTypes:
                self.playerGameDataInitialization()

        # Case 2: transform raw data to final
        elif self.actionType == "T":
            logging.info("Initializing Local Data Through Pipeline")
            if "Schedule" in self.dataTypes:
                self.scheduleDataTransformer()

    def scheduleDataInitialization(self):
        logging.info("Beginning Schedule Data Scrapping")
        try:
            currentSeasonInt = int(os.environ.get("CURRENT_SEASON_YEAR"))
            scheduleDataScrapper.scrapeNFLScheduleForRange(2002, currentSeasonInt)
        except Exception as e:
            logging.error("Schedule Scrapping FAILED", e)
            exit()
        logging.info("Scrapped Schedule Data Successful!")

    def playerGameDataInitialization(self):
        logging.info("Beginning Player/Game Data Scrapping")
        try:
            beginningSeasonInt = int(os.environ.get("ANALYTICS_HIST_BEGIN_YEAR"))
            currentSeasonInt = int(os.environ.get("CURRENT_SEASON_YEAR"))
            gameDataScrapper.gameDataScrappingManager(beginningSeasonInt, currentSeasonInt)
        except Exception as e:
            logging.error("Schedule Scrapping FAILED", e)
            exit()
        logging.info("Scrapped Player/Game Data Successful!")

    def scheduleDataTransformer(self):
        logging.info('Beginning Schedule Data Transformation')
        try:
            scheduleDataTransformer.transformScheduleData()
        except Exception as e:
            logging.error("Transforming Schedule Data FAILED", e)
            exit()
        logging.info("Transformed Schedule Data Successful!")
