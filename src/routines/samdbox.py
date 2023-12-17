import logging
import os
from datetime import datetime

import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.functions.data.dfs.bdb.bdbDataRetrievalFuncs import getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName
from src.functions.data.msf.game import gameDataFuncs
from src.functions.data.msf.player.playerDataFuncs import getMSFPlayerDataByYearWeekGameTeamName, getMSFPlayerDataByYearWeekTeamName
from src.functions.data.msf.venue import venueDataFuncs
from src.functions.nflFuncs import getWeeksInSeason
from src.routines.dkContestParticipantBridgeRoutines.mainDKContestParticipantBridgeCreationRoutine import generatePlayerIDBridgeForSeasonWeekGameTeam
from src import constants

apiDataYearStart = int(os.getenv("FIRST_API_SEASON_YEAR"))
apiDataYearEnd = int(os.getenv("CURRENT_SEASON_YEAR"))
currentLastWeekNum = int(os.getenv("CURRENT_SEASON_LAST_COMPLETED_WEEK"))
absProjectFilepath = os.getenv("ABS_PROJECT_PATH")




def getDFDataByColumns(gameEntry, colArr):
    valuesDict = {}
    for colName in colArr:
        valuesDict[colName] = gameEntry[colName]
    return pd.DataFrame([valuesDict])

# print(pd.DataFrame([{1: "1", 2: "2", 3: "3"}]))
# print(getDFDataByColumns([2, 3])
# exit()


def findBDBRecord(msfTeamName, bdbTeamData):
    for i,bdbEntry in bdbTeamData.iterrows():
        bdbTeamName = bdbEntry["Player Team"]
        if bdbTeamName == msfTeamName:
            return bdbEntry


def bridgeTeamDataEntries(msfTeamData, bdbTeamData, year, week):
    for i,msfEntry in msfTeamData.iterrows():
        msfTeamName = msfEntry["#Team City"] + " " + msfEntry['#Team Name']
        bdbRecord = findBDBRecord(msfTeamName, bdbTeamData)
        df = pd.DataFrame([msfEntry.to_dict() | bdbRecord.to_dict()], index=None)
        return df
    return None


def getMSFTeamEntry(year, week, teamName):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/msf/weekly_team_game_logs/"
    filepath = absProjectPath + targetDirectory + str(year) + '/' + str(week) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    df = df.loc[df["#Team City"] + " " + df['#Team Name'] == teamName]
    df = df.sort_values(by=['#Team Name']).reset_index()
    return df


def getBDBTeamEntry(year, week, teamName):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")
    targetDirectory = "data/dfs/historicalDFSPlayerResults/csv/"
    filepath = absProjectPath + targetDirectory + str(year) + '.csv'
    df = pd.read_csv(filepath, index_col=False)
    df = df.loc[(df['DK Position'] == "DST") & (df["Week"] == week) & (df["Player Name"] == teamName)]
    df = df.sort_values(by=['Player Name']).reset_index()
    return df



def getMSFandBDBTeamEntryByYearWeekTeamName(year, week, teamName):
    msfTeamData = getMSFTeamEntry(year, week, teamName)
    bdbTeamData = getBDBTeamEntry(year, week, teamName)
    combinedTeamEntry = bridgeTeamDataEntries(msfTeamData, bdbTeamData, year, week)
    if type(combinedTeamEntry) == pd.DataFrame:
        combinedTeamEntry["PlayerDK200ptSalaryEff"] = round((combinedTeamEntry["DK Salary"]/50000) * combinedTeamEntry["DK Points"], 2)
        df = combinedTeamEntry.sort_values(by=['PlayerDK200ptSalaryEff'], ascending=True)
        eff = df['PlayerDK200ptSalaryEff'].values
        df["PlayerDKEffLabel"] = 0
        if eff >= .7:
            df["PlayerDKEffLabel"] = 1
        return combinedTeamEntry
    else:
        logging.info([str(year), str(week), teamName, "BDB TEAM NOT BRIDGED/FOUND FOR MSF TEAM"])



def getTemporalTeamData(temporalArr, year, week, teamName, teamMap):
    allTemporalResults = []
    largestRangeEntryAVG = None
    temporalEntryCounter = 0
    for temporalValue in temporalArr:
        print(temporalValue)
        weeksIntoPast = temporalValue
        currentWeek = week
        temporalWeek = week - weeksIntoPast

        temporalWeeksDFs = []
        ### retrieve all week team values
        for weekNum in range(temporalWeek, currentWeek):
            if teamName in teamMap[str(year)][str(weekNum)].keys():
                sr = teamMap[str(year)][str(weekNum)][str(teamName)]
                temporalWeeksDFs.append(sr)
            else:  # bye week
                temporalWeeksDFs.append(None)

        ### filter out bye weeks
        filteredTemporalWeeksDF = []
        for entry in temporalWeeksDFs:
            if type(entry) == None:
                continue
            else:
                filteredTemporalWeeksDF.append(entry)

        ### split by num and cat
        ### convert cat
        ### avg num and cat


        quit()

        if temporalEntryCounter == 0: # save first entry as avg for fill ins
            largestRangeEntry = df
        temporalEntryCounter+=1


    # constants.tDNumCols  ################################################################################################# decide on how to average categorical and numerical data (big deal! one of the last few challenges)
    # constants.tDCatCols
    #
    # dfCatConverted = convertCatDFValues(dfCat, dfCat.columns)
    #
    # print(dfCatConvertedAVG)
    # exit()

    # temporalWeekDFs.append(df)
    # dfNumAVG = dfNum['mean'] = dfNum.mean(axis=1)
    # dfCatConvertedAVG = dfCatConverted['mean'] = dfCatConverted.mean(axis=1)




    quit()



# def createTTEntries(ttData):
#     pass
#
#
# def adjustTemporalColsArr(temporalArr, ttDNumericCols):
#     pass
#
#
# def getTemporalPlayerData(temporazArr):
#     pass
#
#
# def createPTEntries(ptData):
#     pass


def createAllSeasonsTrainingData(temporalArr, trainingWeekRangeStart, trainingWeekRangeEnd):
    gameMap, teamMap, playerMap = {}, {}, {}

    allPlayerFinalEntries = []
    allTeamFinalEntries = []

    for year in range(apiDataYearStart, apiDataYearEnd + 1):  # for year
        totalSeasonWeeks = getWeeksInSeason(year)
        gameMap[str(year)] = {}
        teamMap[str(year)] = {}
        playerMap[str(year)] = {}

        for week in range(1, totalSeasonWeeks + 1):  # for week
            if year < apiDataYearEnd or (year == apiDataYearEnd and week <= currentLastWeekNum):  # if week is in all stored data range
                msfYearWeekGamesRecords = gameDataFuncs.getMSFGameDataByYearWeek(year, week)
                gameMap[str(year)][str(week)] = {}
                teamMap[str(year)][str(week)] = {}
                playerMap[str(year)][str(week)] = {}

                for i, gameEntry in msfYearWeekGamesRecords.iterrows():  # for game
                    venueID = gameEntry['#Venue ID']
                    homeTeamName = gameEntry["#Home Team City"] + " " + gameEntry['#Home Team Name']
                    awayTeamName = gameEntry["#Away Team City"] + " " + gameEntry['#Away Team Name']
                    teamNames = [homeTeamName, awayTeamName]
                    print(year, week, teamNames)

                    venueEntry = None
                    if trainingWeekRangeStart <= week <= trainingWeekRangeEnd:  # build model training entry values
                        venueEntry = venueDataFuncs.getVenueEntryByID(venueID)

                    for index in range(0, len(teamNames)):
                        # set up logging
                        logging.basicConfig(filename=os.getenv("ABS_PROJECT_PATH") + 'logs/bdbtomsfTeamIDBridge.log', filemode='w',
                                            level=logging.DEBUG)

                        # add team data to team map
                        ### TODO: INJURY DATA # iDNumCols # iDCatCols
                        teamEntry = getMSFandBDBTeamEntryByYearWeekTeamName(year, week, teamNames[index])
                        teamMap[str(year)][str(week)].update({str(teamNames[index]): teamEntry})
                        playerMap[str(year)][str(week)][str(teamNames[index])] = {}

                        ttData=None
                        if trainingWeekRangeStart <= week <= trainingWeekRangeEnd:  # build team DST model training entry
                            ### get team current week + temporal values and columns
                            # ttData = getTemporalTeamData(temporalArr, year, week, str(teamNames[index]), teamMap)
                            ttData = getTemporalTeamData(temporalArr, year, week, str(teamNames[index]), teamMap)
                            #########################################################################################
                            allTeamFinalEntries.append(pd.concat([venueEntry, gameEntry, ttData], axis=0))
                            print(ttData)
                            quit()


                        # bridge year week team players data
                        bdbDF = getBDBDFSDHistoricalPlayerResultsByYearWeekTeamName(year, week, teamNames[index])  # get bdb player data
                        msfDF = getMSFPlayerDataByYearWeekTeamName(year, week, teamNames[index])  # get msf player data
                        playerSeasonWeekTeamMatchRecords = generatePlayerIDBridgeForSeasonWeekGameTeam(bdbDF, msfDF, year, week)

                        for playerBridgedEntry in playerSeasonWeekTeamMatchRecords:  # for bridged player
                            universalPlayerName = playerBridgedEntry["upnID"]
                            playerMap[str(year)][str(week)][str(teamNames[index])].update({str(universalPlayerName): playerBridgedEntry})  # save now, scale later

                            ### build player model training entry
                            if trainingWeekRangeStart <= week <= trainingWeekRangeEnd:
                                ### get player current week + temporal columns and values
                                ptData = getTemporalPlayerData(temporalArr)
                                #######################################################################################
                                allPlayerFinalEntries.append(pd.concat([venueEntry, gameEntry, ttData, ptData], axis=0))



    return allPlayerFinalEntries, allTeamFinalEntries

def scalePlayerFinalEntries(allPlayerFinalEntries, temporalArr):
    # get numerical data
    venueNum = getDFDataByColumns(allPlayerFinalEntries, constants.vDNumCols)

    gameNum = getDFDataByColumns(allPlayerFinalEntries, constants.gDNumCols)

    teamTempColsNum = constants.convertColumnsToTemporal(constants.ttDNumCols , temporalArr)
    teamTempNum = getDFDataByColumns(allPlayerFinalEntries, teamTempColsNum)

    playerTempColsNum = constants.convertColumnsToTemporal(constants.ptDNumCols, temporalArr)
    playerTempNum = getDFDataByColumns(allPlayerFinalEntries, playerTempColsNum)

    allNum = pd.concat([venueNum, gameNum, teamTempNum, playerTempNum], axis=0)

    # scale numerical
    scaler = MinMaxScaler()
    allNumDF = scaler.fit_transform(allNum)

    # save scalar
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    scalerFilepath = absProjectFilepath + "mlModels/playerEfficiencyFilterModels/scalars/player/" + str(dt_string) + ".save"
    joblib.dump(scaler, scalerFilepath)

    # get categorical data
    venueCat = getDFDataByColumns(allPlayerFinalEntries, constants.vDCatCols)

    gameCat = getDFDataByColumns(allPlayerFinalEntries, constants.gDCatCols)

    teamTempColsCat = constants.convertColumnsToTemporal(constants.ttDNumCols, temporalArr)
    teamTempCat = getDFDataByColumns(allPlayerFinalEntries, teamTempColsCat)

    playerTempColsCat = constants.convertColumnsToTemporal(constants.ttDNumCols, temporalArr)
    playerTempCat = getDFDataByColumns(allPlayerFinalEntries, playerTempColsCat)

    allCat = pd.concat([venueCat, gameCat, teamTempCat, playerTempCat], axis=0)

    # convert categorical
    catDict = {}
    for columnName in allCat.columns:
        columnValue = allCat[columnName]
        convertedValue = constants.convertCatColumnToValues(columnName, columnValue)
        catDict.update({columnName: convertedValue})
    allCatDF = pd.DataFrame([catDict], index=None)



    # return all scaled player entries
    allEntries = pd.concat([allNumDF, allCatDF], axis=0)
    return allEntries

def scaleTeamFinalEntries(allTeamFinalEntries, temporalArr):
    # get numerical data
    venueNum = getDFDataByColumns(allTeamFinalEntries, constants.vDNumCols)

    gameNum = getDFDataByColumns(allTeamFinalEntries, constants.gDNumCols)

    teamTempColsNum = constants.convertColumnsToTemporal(constants.ttDNumCols, temporalArr)
    teamTempNum = getDFDataByColumns(allTeamFinalEntries, teamTempColsNum)

    allNum = pd.concat([venueNum, gameNum, teamTempNum], axis=0)

    # convert numerical


    # get categorical data
    venueCat = getDFDataByColumns(allTeamFinalEntries, constants.vDCatCols)

    gameCat = getDFDataByColumns(allTeamFinalEntries, constants.gDCatCols)

    teamTempColsCat = constants.convertColumnsToTemporal(constants.ttDNumCols, temporalArr)
    teamTempCat = getDFDataByColumns(allTeamFinalEntries, teamTempColsCat)


    allCat = pd.concat([venueCat, gameCat, teamTempCat], axis=0)

    # convert categorical


    # return all scaled player entries
    allEntries = pd.concat([allNum, allCat], axis=0)
    return allEntries

# temp arr
temporalArr = [5, 3, 1]
allPlayerFinalEntries, allTeamFinalEntries = createAllSeasonsTrainingData(temporalArr, 6, 16)
finalPlayerData = scalePlayerFinalEntries(allPlayerFinalEntries, temporalArr)
finalTeamData = scaleTeamFinalEntries(allTeamFinalEntries, temporalArr)
#
# x_train, x_test, y_train, y_test = train_test_split(dataInputScaled, dataOutputScaled, test_size=0.2)
# model = tf.keras.models.Sequential()
# model.add(keras.layers.Dense(units=64, activation=tf.keras.activations.relu, input_shape=(12,)))
# model.add(keras.layers.Dense(units=64, activation=tf.keras.activations.relu))
# model.add(keras.layers.Dense(units=1, activation=tf.keras.activations.sigmoid))
#
# model.compile(optimizer=tf.keras.optimizers.Adam(),
#               loss=tf.keras.losses.MeanSquaredError(),
#               metrics=['accuracy'])
#
#
# model.fit(x_train, y_train, epochs=50, batch_size=50, validation_split=0.2)
#
# test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
#
# print('\nTest accuracy:', test_acc)
#
# y_predict = model.predict(x_test)
# # for i in range(0, len(x_test)):
# #     print(x_test[i])
# #     print(y_test[i])
# #     print(y_predict[i])
# #     y_predict_original = scaler.inverse_transform(y_predict)
# #     print("\n")
#
# y_predict_original = scaler.inverse_transform(y_predict)
# y_test_original = scaler.inverse_transform(y_test)
#
# from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
# n = len(x_test)
# k = x_test.shape[1]
# RMSE = float(format(np.sqrt(mean_squared_error(y_test_original, y_predict_original)), '0.3f'))
# MSE = mean_squared_error(y_test_original, y_predict_original)
# MAE = mean_absolute_error(y_test_original, y_predict_original)
# r2 = r2_score(y_test_original, y_predict_original)
# adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1)
# print('RMSE =', RMSE, '\nMSE =', MSE, '\nMAE =', MAE, '\nR2 =', r2, '\nAdjusted R2 =', adj_r2)
#
# # trainingData = [test_acc, r2, "singleGameV1", "singleGame", str(datetime.datetime.now()), modelFilepath, scalerFilepath]
# # trainingMethodInfoFilepath = absProjectPath + "analysis/trainedMethodInfo.csv"
# # arr = pd.read_csv(trainingMethodInfoFilepath, header=None).to_numpy().tolist()
# # arr.append(trainingData)
# # cols = ["Accuracy", "R2", "ModelName", "DataType", "DatetimeTrained", "ModelFilepath", "ScalarFilepath"]
# # pd.DataFrame(arr).to_csv(trainingMethodInfoFilepath, columns=cols)
#
# # format test analysis variables
# fAdj_R2 = str(round(adj_r2*100, 2))
# fTestAcc = str(round(test_acc * 100, 2))
#
# # save trained model
# modelFilepath = absProjectPath + "analysis/singleGame/models/" + "_" + fTestAcc + "_" + fAdj_R2 + "_" + str(todaysDate) + "_" + str(predictionStartDate) + "_" + str(predictionEndDate) + ".keras"
# model.save(modelFilepath)

