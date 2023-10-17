import os

import pandas as pd
import tensorflow as tf
import joblib
import sys
from src.dataLoaders.scheduleDataLoaders import getFinalScheduleTrainingData
from src.dataPipeline.dataTransformers.scheduleDataTransformer import transformScheduleData

class PredictorModel:
    def predictScheduleDataOutcomes(self, modelName, predictionStartDate, predictionEndDate):
        """
        :param modelName: the name of the pre-trained model being tested
        :param predictionStartDate: the beginning date of outcomes to be predicted
        :param predictionEndDate: the final date of outcomes to be predicted
        :return:
        """
        absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
        ### TODO: insert filename determiner for modelname
        # modelInfoFilepath = "analysis/Single_Game_Outcome_Schedule_Data/modelInfo/modelTrainingInfo.csv"
        # pd.read_csv(modelInfoFilepath)  # dynamic model selection based on training dates
        modelFilepath = absProjectFilepath + "analysis/singleGame/models/_74.4_31.05_2023-10-16_2002-06-01_2023-06-01.keras"
        scalerFilepath = absProjectFilepath + "analysis/singleGame/scalers/_74.4_31.05_2023-10-16_2002-06-01_2023-06-01.save"

        finalScheduleData = getFinalScheduleTrainingData(predictionStartDate, predictionEndDate)[0]
        model = tf.keras.models.load_model(modelFilepath)
        savedScalar = joblib.load(scalerFilepath)

        gamesPredicted = 0
        gamesPredictedCorrect = 0
        for i in range(0, len(finalScheduleData)):
            # scale input prediction data to pretrained model
            predictionDataArr = [finalScheduleData[i][7], finalScheduleData[i][8], finalScheduleData[i][9],
                                 finalScheduleData[i][10], finalScheduleData[i][11], finalScheduleData[i][12],
                                 finalScheduleData[i][14],
                                 finalScheduleData[i][15], finalScheduleData[i][16], finalScheduleData[i][17],
                                 finalScheduleData[i][18], finalScheduleData[i][19]]
            predictionData = pd.DataFrame(predictionDataArr, index=None)
            formattedPredictionData = predictionData.iloc[:, ].values
            scaledPredictionData = savedScalar.fit_transform(formattedPredictionData)  # yards not scaled correctly

            # get data from the wacky formatted scaledPredictionData
            scaledPredictionDataArr = []
            for statIndex in range(0, len(predictionDataArr)):
                scaledPredictionDataArr.append([scaledPredictionData[statIndex][0]])
            prediction = model.predict(
                [scaledPredictionDataArr])  # https://www.pro-football-reference.com/teams/rai/2023.htm
            normalizedPrediction = savedScalar.inverse_transform(prediction)
            # print("Prediction: ", prediction)
            # print("Normalized Prediction: ", normalizedPrediction)

            homeIsWinner = finalScheduleData[i][5]
            homeTeamName = finalScheduleData[i][24]
            homeTeamScore = finalScheduleData[i][20]
            awayTeamName = finalScheduleData[i][25]
            awayTeamScore = finalScheduleData[i][21]
            outString = ""
            if prediction >= 0.5:
                if homeIsWinner == 0:
                    outString = homeTeamName + " predicted to win, they did NOT beat " + awayTeamName
                else:
                    outString = homeTeamName + " predicted to win, they beat " + awayTeamName
                    gamesPredictedCorrect += 1

            elif prediction < 0.5:
                if homeIsWinner == 1:
                    outString = awayTeamName + " predicted to win, they did NOT beat " + homeTeamName
                else:
                    outString = awayTeamName + " predicted to win, they beat " + homeTeamName
                    gamesPredictedCorrect += 1
            print(outString)
            gamesPredicted += 1

            print("\n")
        print(gamesPredicted, gamesPredictedCorrect)
        print("Accuracy: " + str(round(gamesPredictedCorrect / gamesPredicted, 2) * 100) + "%")

model = PredictorModel()
# model.predictScheduleDataOutcomes("ignore", "2023-10-04", "2023-10-10")
model.predictScheduleDataOutcomes("ignore", "2023-10-10", "2023-10-17")