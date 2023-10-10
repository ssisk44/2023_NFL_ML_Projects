"""
### SGO_V1 Description
This is the absolute bare minimum single game prediction based off of solely schedule data. This should provide a
strong baseline for reflecting on the outcomes of more advanced models.
"""
import datetime
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from src.utilityFunctions import getProcessedScheduleData
from src.teamNaming import getTeamFranchiseInt
from statistics import mean
import keras.api._v2.keras as keras
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

finalCols = ["season", "weekNum", "isDayGame", "isPrimetime", "isPlayoffs", "homeIsWinner", "homeFranchiseInt",
             "homeOffPointsAvg", "homeOffYardsAvg", "homeOffTOAvg", "homeDefPointsAvg", "homeDefYardsAvg",
             "homeDefTOAvg", "awayFranchiseInt", "awayOffPointsAvg", "awayOffYardsAvg", "awayOffTOAvg",
             "awayDefPointsAvg", "awayDefYardsAvg", "awayDefTOAvg", "Home Score", "Away Score", "Score Diff"]


def main():
    """
    These are the two core operations performed here:
    1) Extra data prep -> needs to be moved to dataManipulator
    2) training a model
    """
    #prepare data
    df,ignore = prepareDataForModel("2002-01-01", "2023-06-01")

    #train model
    trainModel(df)


def getGamesBySeason(seasonsGamesArr, seasonYear):
    seasonGames = []
    for game in seasonsGamesArr:
        if game[0] == seasonYear:
            seasonGames.append(game)
        if game[0] > seasonYear:
            break
    return seasonGames


def calculateSeasonAverage(seasonGames):
    homeTeamPPG = []
    homeTeamYPG = []
    homeTeamTOPG = []
    awayTeamPPG = []
    awayTeamYPG = []
    awayTeamTOPG = []
    for game in seasonGames:
        homeTeamPPG.append(game[7])
        homeTeamYPG.append(game[8])
        homeTeamTOPG.append(game[9])
        awayTeamPPG.append(game[11])
        awayTeamYPG.append(game[12])
        awayTeamTOPG.append(game[13])
    return [homeTeamPPG, homeTeamYPG, homeTeamTOPG, awayTeamPPG, awayTeamYPG, awayTeamTOPG]


def createStatMap(allSeasonsGames, startYear, endYear):
    # STAT AVERAGING
    offensivePoints = {}
    offensiveYards = {}
    offensiveTO = {}
    defensivePoints = {}
    defensiveYards = {}
    defensiveTO = {}

    for year in range(int(startYear), int(endYear)+1):
        # initialize data year for entries
        offensivePoints[year] = {}
        offensiveYards[year] = {}
        offensiveTO[year] = {}
        defensivePoints[year] = {}
        defensiveYards[year] = {}
        defensiveTO[year] = {}

        seasonGames = getGamesBySeason(allSeasonsGames, year)

        for game in seasonGames:
            season = game[0]
            week = game[1]
            homeTeamName = game[6]
            homeTeamPoints = game[7]
            homeTeamYards = game[8]
            homeTeamTO = game[9]
            awayTeamName = game[10]
            awayTeamPoints = game[11]
            awayTeamYards = game[12]
            awayTeamTO = game[13]

            teamNameMap = offensivePoints[season].keys()
            if homeTeamName not in teamNameMap:
                offensivePoints[season][homeTeamName] = [homeTeamPoints]
                offensiveYards[season][homeTeamName] = [homeTeamYards]
                offensiveTO[season][homeTeamName] = [homeTeamTO]
                defensivePoints[season][homeTeamName] = [awayTeamPoints]
                defensiveYards[season][homeTeamName] = [awayTeamYards]
                defensiveTO[season][homeTeamName] = [awayTeamTO]
            else:
                offensivePoints[season][homeTeamName].append(homeTeamPoints)
                offensiveYards[season][homeTeamName].append(homeTeamYards)
                offensiveTO[season][homeTeamName].append(homeTeamTO)
                defensivePoints[season][homeTeamName].append(awayTeamPoints)
                defensiveYards[season][homeTeamName].append(awayTeamYards)
                defensiveTO[season][homeTeamName].append(awayTeamTO)

            if awayTeamName not in teamNameMap:
                offensivePoints[season][awayTeamName] = [awayTeamPoints]
                offensiveYards[season][awayTeamName] = [awayTeamYards]
                offensiveTO[season][awayTeamName] = [awayTeamTO]
                defensivePoints[season][awayTeamName] = [homeTeamPoints]
                defensiveYards[season][awayTeamName] = [homeTeamYards]
                defensiveTO[season][awayTeamName] = [homeTeamTO]

            else:
                offensivePoints[season][awayTeamName].append(awayTeamPoints)
                offensiveYards[season][awayTeamName].append(awayTeamYards)
                offensiveTO[season][awayTeamName].append(awayTeamTO)
                defensivePoints[season][awayTeamName].append(homeTeamPoints)
                defensiveYards[season][awayTeamName].append(homeTeamYards)
                defensiveTO[season][awayTeamName].append(homeTeamTO)

    return [offensivePoints, offensiveYards, offensiveTO, defensivePoints, defensiveYards, defensiveTO]


def returnStatMapValues(year, week, teamName, statMap):
    retValues = []
    for map in statMap:
        if week == 1:
            retValues.append(round(mean(map[year][teamName]), 2))
        else:
            retValues.append(round(mean(map[year][teamName][:week]), 2))
    return retValues


def buildMLArray(allSeasonsGames, statmap):
    mlArr = []

    gameCounter = 0
    for game in allSeasonsGames:
        season = game[0]
        week = game[1]
        homeTeamName = game[6]
        homeTeamFranchiseInt = getTeamFranchiseInt(homeTeamName)
        homeTeamPoints = game[7]
        # homeTeamYards = game[8]
        # homeTeamTO = game[9]
        homeTeamStatMapValues = returnStatMapValues(season, week, homeTeamName, statmap)

        awayTeamName = game[10]
        awayTeamFranchiseInt = getTeamFranchiseInt(awayTeamName)
        awayTeamPoints = game[11]
        # awayTeamYards = game[12]
        # awayTeamTO = game[13]

        gameCounter += 1
        awayTeamStatMapValues = returnStatMapValues(season, week, awayTeamName, statmap)
        arr = [
            game[0],
            game[1],
            game[-4],
            game[-3],
            game[-2],
            game[5],
            homeTeamFranchiseInt,
            homeTeamStatMapValues[0],
            homeTeamStatMapValues[1],
            homeTeamStatMapValues[2],
            homeTeamStatMapValues[3],
            homeTeamStatMapValues[4],
            homeTeamStatMapValues[5],
            awayTeamFranchiseInt,
            awayTeamStatMapValues[0],
            awayTeamStatMapValues[1],
            awayTeamStatMapValues[2],
            awayTeamStatMapValues[3],
            awayTeamStatMapValues[4],
            awayTeamStatMapValues[5],
            homeTeamPoints,
            awayTeamPoints,
            homeTeamPoints - awayTeamPoints
        ]
        mlArr.append(arr)

    h = [
        "season",
        "weekNum",
        "isDayGame",
        "isPrimetime",
        "isPlayoffs",
        "homeIsWinner",
        "homeFranchiseInt",
        "homeOffPointsAvg",
        "homeOffYardsAvg",
        "homeOffTOAvg",
        "homeDefPointsAvg",
        "homeDefYardsAvg",
        "homeDefTOAvg",
        "awayFranchiseInt",
        "awayOffPointsAvg",
        "awayOffYardsAvg",
        "awayOffTOAvg",
        "awayDefPointsAvg",
        "awayDefYardsAvg",
        "awayDefTOAvg",
        "Home Score",
        "Away Score",
        "Score Diff",
    ]

    pd.DataFrame(mlArr).to_csv("data/Final/AllSeasonsGamesScheduleData"+str(datetime.datetime.now()).replace("-","").replace(":","").replace(" ","")+".csv", header=h, index=False)
    return mlArr


def trainModel(df):
    time = str(datetime.date.today())

    # x_numerical = df[["season","weekNum", "homeFranchiseInt","homeOffPointsAvg","homeOffYardsAvg","homeOffTOAvg","homeDefPointsAvg","homeDefYardsAvg","homeDefTOAvg","awayFranchiseInt","awayOffPointsAvg","awayOffYardsAvg","awayOffTOAvg","awayDefPointsAvg","awayDefYardsAvg","awayDefTOAvg","Home Score","Away Score", "Score Diff"]]
    x_numerical = df[["homeOffPointsAvg", "homeOffYardsAvg", "awayOffPointsAvg", "awayOffYardsAvg", "homeIsWinner"]]
    # x_categorical = df[['isDayGame', 'isPrimetime', 'isPlayoffs']]

    onehotencoder = OneHotEncoder()
    # x_categorical = onehotencoder.fit_transform(x_categorical).toarray()
    # x_categorical = pd.DataFrame(x_categorical)
    # x_all = pd.concat([x_categorical, x_numerical], axis=1)

    dataInput = x_numerical.iloc[:, :-1].values
    dataOutput = x_numerical.iloc[:, -1:].values

    scaler = MinMaxScaler()
    dataInputScaled = scaler.fit_transform(dataInput)

    scaler_filename = "analysis/Single_Game_Outcome_Schedule_Data/models/SGOSD_V1_Model_" + time + "_scaler.save"
    joblib.dump(scaler, scaler_filename)

    dataOutputScaled = scaler.fit_transform(dataOutput)

    x_train, x_test, y_train, y_test = train_test_split(dataInputScaled, dataOutputScaled, test_size=0.1)
    model = tf.keras.models.Sequential()
    model.add(keras.layers.Dense(units=512, activation=tf.keras.activations.relu, input_shape=(4,)))
    model.add(keras.layers.Dense(units=512, activation=tf.keras.activations.relu))
    model.add(keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.save("analysis/Single_Game_Outcome_Schedule_Data/models/SGOSD_V1_Model_" + time + ".keras")

    model.fit(x_train, y_train, epochs=50, batch_size=25, validation_split=0.1)

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)

    print('\nTest accuracy:', test_acc)

    y_predict = model.predict(x_test)
    # for i in range(0, len(x_test)):
    #     print(x_test[i])
    #     print(y_test[i])
    #     print(y_predict[i])
    #     y_predict_original = scaler.inverse_transform(y_predict)
    #     print(y_predict_original[i])
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


def prepareDataForModel(predictionStartDate, predictionEndDate):
    allSeasonsGames = getProcessedScheduleData(predictionStartDate, predictionEndDate)

    statMap = [offensivePointsMap, offensiveYardsMap, offensiveTOMap, defensivePointsMap, defensiveYardsMap,
               defensiveTOMap] = createStatMap(allSeasonsGames, predictionStartDate[0:4], predictionEndDate[0:4])
    finalMLDataArray = buildMLArray(allSeasonsGames, statMap)
    df = pd.DataFrame(finalMLDataArray, columns=finalCols)
    return allSeasonsGames, df
