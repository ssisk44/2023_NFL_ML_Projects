"""
### scheduleModelTrainerV1 Description
This is the absolute bare minimum single game prediction based off of solely schedule data. This should provide a
strong baseline for reflecting on the outcomes of more advanced models.
"""
import datetime
import os
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
import keras.api._v2.keras as keras
from src.dataLoaders.scheduleDataLoaders import getFinalScheduleTrainingData
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def trainSingleGameV1Model(predictionStartDate, predictionEndDate):
    import dotenv
    dotenv.load_dotenv()
    absProjectPath = str(os.getenv("ABS_PROJECT_PATH"))
    todaysDate = str(datetime.date.today())

    # get data
    allSeasonsGames, df = getFinalScheduleTrainingData(predictionStartDate, predictionEndDate)

    x_numerical = df[
        ["homeOffPointsAvg", "homeOffYardsAvg", "homeOffTOAvg", "homeDefPointsAvg", "homeDefYardsAvg", "homeDefTOAvg",
         "awayOffPointsAvg", "awayOffYardsAvg", "awayOffTOAvg", "awayDefPointsAvg", "awayDefYardsAvg", "awayDefTOAvg",
         "homeIsWinner"]]

    # x_categorical = df[['isDayGame', 'isPrimetime', 'isPlayoffs']]
    # x_numerical = df[["season","weekNum", "homeFranchiseInt","homeOffPointsAvg","homeOffYardsAvg","homeOffTOAvg","homeDefPointsAvg","homeDefYardsAvg","homeDefTOAvg","awayFranchiseInt","awayOffPointsAvg","awayOffYardsAvg","awayOffTOAvg","awayDefPointsAvg","awayDefYardsAvg","awayDefTOAvg","Home Score","Away Score", "Score Diff"]]

    # onehotencoder = OneHotEncoder()
    # x_categorical = onehotencoder.fit_transform(x_categorical).toarray()
    # x_categorical = pd.DataFrame(x_categorical)
    # x_all = pd.concat([x_categorical, x_numerical], axis=1)

    dataInput = x_numerical.iloc[:, :-2].values
    dataOutput = x_numerical.iloc[:, -2:-1].values

    scaler = MinMaxScaler()
    dataInputScaled = scaler.fit_transform(dataInput)

    dataOutputScaled = scaler.fit_transform(dataOutput)

    x_train, x_test, y_train, y_test = train_test_split(dataInputScaled, dataOutputScaled, test_size=0.2)
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Dense(units=64, activation=tf.keras.activations.relu, input_shape=(12,)))
    model.add(keras.layers.Dense(units=64, activation=tf.keras.activations.relu))
    model.add(keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.MeanSquaredError(),
                  metrics=['accuracy'])


    model.fit(x_train, y_train, epochs=50, batch_size=50, validation_split=0.2)

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)

    print('\nTest accuracy:', test_acc)

    y_predict = model.predict(x_test)
    # for i in range(0, len(x_test)):
    #     print(x_test[i])
    #     print(y_test[i])
    #     print(y_predict[i])
    #     y_predict_original = scaler.inverse_transform(y_predict)
    #     print("\n")

    y_predict_original = scaler.inverse_transform(y_predict)
    y_test_original = scaler.inverse_transform(y_test)

    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    n = len(x_test)
    k = x_test.shape[1]
    RMSE = float(format(np.sqrt(mean_squared_error(y_test_original, y_predict_original)), '0.3f'))
    MSE = mean_squared_error(y_test_original, y_predict_original)
    MAE = mean_absolute_error(y_test_original, y_predict_original)
    r2 = r2_score(y_test_original, y_predict_original)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
    print('RMSE =', RMSE, '\nMSE =', MSE, '\nMAE =', MAE, '\nR2 =', r2, '\nAdjusted R2 =', adj_r2)

    # trainingData = [test_acc, r2, "singleGameV1", "singleGame", str(datetime.datetime.now()), modelFilepath, scalerFilepath]
    # trainingMethodInfoFilepath = absProjectPath + "analysis/trainedMethodInfo.csv"
    # arr = pd.read_csv(trainingMethodInfoFilepath, header=None).to_numpy().tolist()
    # arr.append(trainingData)
    # cols = ["Accuracy", "R2", "ModelName", "DataType", "DatetimeTrained", "ModelFilepath", "ScalarFilepath"]
    # pd.DataFrame(arr).to_csv(trainingMethodInfoFilepath, columns=cols)

    # format test analysis variables
    fAdj_R2 = str(round(adj_r2*100, 2))
    fTestAcc = str(round(test_acc * 100, 2))

    # save trained model
    modelFilepath = absProjectPath + "analysis/singleGame/models/" + "_" + fTestAcc + "_" + fAdj_R2 + "_" + str(todaysDate) + "_" + str(predictionStartDate) + "_" + str(predictionEndDate) + ".keras"
    model.save(modelFilepath)

    # save trained model data scaler
    scalerFilepath = absProjectPath + "analysis/singleGame/scalers/" + "_" + fTestAcc + "_" + fAdj_R2 + "_" + str(todaysDate) + "_" + str(predictionStartDate) + "_" + str(predictionEndDate) + ".save"
    joblib.dump(scaler, scalerFilepath)

trainSingleGameV1Model("2002-06-01", "2023-06-01")
trainSingleGameV1Model("2002-06-01", "2023-06-01")
trainSingleGameV1Model("2002-06-01", "2023-06-01")
trainSingleGameV1Model("2002-06-01", "2023-06-01")
trainSingleGameV1Model("2002-06-01", "2023-06-01")