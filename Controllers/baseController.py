import controllers.modelTrainingController as ModelTrainingController
import logging
import dotenv
from models.DataPipelineModel import DataPipeline
################################################################################
######                                                                    ######
#  This should be the first code hit when this script is loaded onto a server  #
######                                                                    ######
################################################################################


class BaseController:
    def __init__(self, requestType, dataTypes, actionType, args):
        """
       :param requestType (Pipeline "PI", Model Training "MT", Prediction "PR", "Dashboard", "DFS"):
       :param dataTypes ("Schedule", "Game", "PlayerGame", "PlayerBio", "Team", "Injury", "Weather", "Depth Chart"):
       :param actionType ("I", "U", "T"): initialize/update/transform local dataset
       :param {} args:
       """
        self.requestType = requestType
        self.dataTypes = dataTypes
        self.actionType = actionType
        self.args = args

        # initialize environment variables
        dotenv.load_dotenv()

        # initialize logging output
        logging.basicConfig(filename='../logs/logs.log', filemode='w', level=logging.DEBUG)

    def performRequest(self):
        logging.info("Beginning Request Processing")
        # handle pipeline requests
        if self.requestType == "PI":
            pipeline = DataPipeline(self.requestType, self.dataTypes, self.actionType)
            pipeline.handlePipelineRequest()

        # handle model training requests
        elif self.requestType == "MT":
            self.completeModelTrainingRequest()

        # handle data prediction requests
        elif self.requestType == "PR":
            self.completeDataPredictionRequest()

        logging.info("Request Process Successful!")


    def completeModelTrainingRequest(self):
        # TODO: PENDING - add training date range, option to exclude week 1?
        ModelTrainingController.completeRequest([self.dataTypes])

    def completeDataPredictionRequest(self):
        # TODO: PENDING - add predictions for date range not exceeding current week + 1
        # if len(self.args.values()) > 0 and "gameIDs" not in self.args.values():
        #     gameIDs = self.args["gameIDs"]
        #     DataAnalysisController.completeRequest([gameIDs, self.dataTypes])
        # else:
        #     raise Exception("No Games Found While Predicting")
        None


    # def completeDashboardRequest(self):
    #     """ TODO: HOSTED - Used to procure real time data on cron schedules, processes, and model accuracies per training date """


    # def parseRequest(self):
    #     """TODO: HOSTED - parse incoming HTML request"""
    #     #  preprocessing/data cleaning should be done in parseRequest
    #     # if len(self.requestType.replace(" ", "")) > 0:
