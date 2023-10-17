import os
import sys
import logging
import pandas as pd
from analysis.singleGame import singleGameV1

class TrainingSchemaModel:
    """ Model Training Object
    - preload all analysis models
    """

    def __init__(self, modelName, modelDataType, trainingStartDate, trainingEndDate, modelArgs):
        self.modelName = modelName  # What name should be recorded for this model
        self.modelDataType = modelDataType  # What data type is being modeled
        self.trainingStartDate = trainingStartDate
        self.trainingEndDate = trainingEndDate
        self.modelArgs = modelArgs  # custom variable array for passing instructions
        self.projectABSFilepath = os.getenv("ABS_PROJECT_PATH")


    def handleTrainingRequest(self):
        """Training a new model"""
        # is a single game model
        if "singleGame" == self.modelDataType:
            if self.modelName == "singleGameV1":
                logging.info("Beginning singleGameV1 Model Training")
                singleGameV1.trainSingleGameV1Model(self.trainingStartDate, self.trainingEndDate)


    def getTrainedModelInfo(self):
        trainingModelInfo = pd.read_csv("../analysis/trainedModelInfo.csv").to_numpy()
        for savedTrainingModel in trainingModelInfo:
            savedModelName = savedTrainingModel[2]
            if savedModelName == self.modelName:
                return savedTrainingModel
        return None

    def runAnalysisOnTrainedModel(self):
        model = self.getTrainedModelInfo()
        modelFilepath = model[-2]
        scalarFilepath = model[-1]

