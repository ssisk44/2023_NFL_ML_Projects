import datetime
import os
import sys

import controllers.scrappingController as ScrappingController
import controllers.dataManipulationController as DataProcessingController
import controllers.analysisController as DataAnalysisController
from src.utilityFunctions import getProcessedScheduleData
from analysis.Single_Game_Outcome_Schedule_Data.versions.SGOSD_V1 import prepareDataForModel
import tensorflow as tf
import joblib
import pandas as pd

def main(testDataAcquisition=False, testCompleteDataProcessing=False, testAnalysis=False):
    ################################################################################
    ######                                                                    ######
    #  This should be the first code hit when this script is loaded onto a server  #
    ######                                                                    ######
    ################################################################################

    ### Note -> find out what time/how long after a game sportsreference uploads game data (scrape at noon everyday?)
    initializeEnvironmentVariables()

    def endpointRunPrediction(modelName, predictionStartDate, predictionEndDate):
        """
        :param modelName: the name of the pre-trained model being tested
        :param predictionStartDate: the beginning date of outcomes to be predicted
        :param predictionEndDate: the final date of outcomes to be predicted
        :return:
        """

        # determine filepath from modelType in modelName
        controlsFilepath = ""
        if "SGOSD" in modelName:
            controlsFilepath = "analysis/Single_Game_Outcome_Schedule_Data/versions/" + modelName + '.py'
            sys.path.insert(0, "analysis/Single_Game_Outcome_Schedule_Data/versions/" + modelName + ".py")
            import analysis.Single_Game_Outcome_Schedule_Data.versions.SGOSD_V1 as Version

        # determine data filepath from modelType
        dataFilepaths = []
        if "SGOSD" in modelName:
            dataFilepaths.append("data/Processed/Schedules/NFLScheduleAndResultsProcessed.csv")

        # determine modelInfo filepath
        modelInfoFilepath = ""
        modelFilepath = ""
        scalerFilepath = ""
        if "SGOSD" in modelName:
            modelInfoFilepath = "analysis/Single_Game_Outcome_Schedule_Data/modelInfo/modelTrainingInfo.csv"
            # pd.read_csv(modelInfoFilepath) # dynamic model selection based on training dates
            modelFilepath = "analysis/Single_Game_Outcome_Schedule_Data/models/SGOSD_V1_Model_2023-10-10.keras"
            scalerFilepath = "analysis/Single_Game_Outcome_Schedule_Data/scalers/SGOSD_V1_Model_2023-10-10_scaler.save"



        # obtain real game data and prediction ready data for cross referencing
        gamesFinal, dfFinal = prepareDataForModel(predictionStartDate, predictionEndDate)
        arrFinal = dfFinal.to_numpy()
        model = tf.keras.models.load_model(modelFilepath)
        savedScalar = joblib.load(scalerFilepath)

        gamesPredicted = 0
        gamesPredictedCorrect = 0
        for i in range(0, len(dfFinal)):
            predictionData = pd.DataFrame([arrFinal[i][6], arrFinal[i][7], arrFinal[i][14], arrFinal[i][15]], index=None)
            formattedPredictionData = predictionData.iloc[:,].values
            scaledPredictionData = savedScalar.fit_transform(formattedPredictionData) # yards not scaled correctly
            # print(scaledPredictionData)
            prediction = model.predict([[scaledPredictionData[0][0], scaledPredictionData[1][0], scaledPredictionData[2][0], scaledPredictionData[3][0]]]) #https://www.pro-football-reference.com/teams/rai/2023.htm
            print("Prediction: ", prediction)
            if prediction >= 0.5:
                outString = "Home Team predicted to win, they did"
                if arrFinal[i][5] == 0:
                    outString += " not."
                else:
                    outString += "!"
                    gamesPredictedCorrect += 1
                print(outString)
            elif prediction < 0.5:
                outString = "Away Team predicted to win, they did"
                if arrFinal[i][5] == 1:
                    outString += " not."
                else:
                    outString += "!"
                    gamesPredictedCorrect += 1
                print(outString)
            gamesPredicted+=1

            # print(prediction)
            print(gamesFinal[i])
            print("\n\n")

        print("Accuracy: " + str(round(gamesPredictedCorrect/gamesPredicted, 2)*100) + "%")


    endpointRunPrediction("SGOSD_V1.py", "2023-09-21", "2023-10-08")







    # the BELOW subsequences are currently performed through manual triggers, this will eventually be moved to a cron
    # TODO: Get the simplest version of this app running on a server with self updating crons/logs with text notifications
    if testDataAcquisition:
        completeDataAcquisition()

    if testCompleteDataProcessing:
        completeDataProcessing()

    if testAnalysis:
        completeDataAnalysis()


def initializeEnvironmentVariables():
    """initializes certain environment variables"""
    ## time
    # now = datetime.datetime.now()
    # os.environ["CURRENT_SEASON_YEAR"] = str(now.year)

def completeDataAcquisition():
    print("Data Acquisition Beginning")
    ScrappingController.main()
    print("Data Acquisition Complete \n")

def completeDataProcessing():
    print("Data Processing Beginning")
    DataProcessingController.main()
    print("Data Acquisition Complete! \n")

def completeDataAnalysis():
    print("Analysis Processes Beginning")
    DataAnalysisController.main()
    print("--- Skipping Analysis Processes \n")




main()
