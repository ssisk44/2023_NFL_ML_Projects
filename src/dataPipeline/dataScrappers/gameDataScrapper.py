import logging
import time
import dotenv
import pandas as pd
import os
from bs4 import BeautifulSoup
from src.dataLoaders.scheduleDataLoaders import getFinalScheduleTrainingData
from src.constants import gamesDataColumns, playersDataColumns
from io import StringIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

"""
For each game in a season get the following information
1) Year - seasonGamesArr
2) Week - seasonGamesArr
3) Date - seasonGamesArr
4) Time - seasonGamesArr
5) Place - seasonGamesArr
6) Away Team - seasonGamesArr
7) Home Team - seasonGamesArr
8) Away Team Score - seasonGamesArr
9) Home Team Score - seasonGamesArr
10) Away Team Season Win % - needs calculation
11) Home Team Season Win % - needs calculation
12) Away Team Coach - scrapping
13) Home Team Coach - scrapping
14) Coin Toss Winner - scrapping
15) Roof - scrapping
16) Surface - scrapping
17) Duration - scrapping
18) Attendance - scrapping
19) Weather Temperature - scrapping
20) Weather Descriptor - scrapping
20) Line - scrapping
21) O/U - scrapping
22) Away Team Rest Days - calculation
23) Home Team Rest Days - calculation
24) Away Team Travel Distance - calculation
25) Home Team Travel Distance - calculation
26) Away Team Consecutive Away Games - calculation
"""


def createChromeDriver():
    options = Options()
    # options.add_argument("--headless=new")
    options.page_load_strategy = 'eager'
    options.add_argument("--start-maximized")
    # options.add_extension('files/5.13.0_0')
    driver = webdriver.Chrome(options=options)
    return driver


def parseScrapedCSVFormatToDF(crudeCSV):
    beginIndex = crudeCSV.index("-->") + 3
    endIndex = crudeCSV.index("</pre>")
    df = pd.read_csv(StringIO(crudeCSV[beginIndex:endIndex]), sep=',')
    return df


def scrapeGameInfo(driver):
    ### GAME INFO
    unformattedGameInfoStats = driver.execute_script("""
        x = document.getElementById("game_info");
        y = x.getElementsByTagName("tbody");

        headerArr = [];
        bodyTextArr = [];
        for (let entryNum = 0; entryNum < y[0].children.length; entryNum++) {
            console.log(entryNum);
            header = y[0].children[entryNum].children[0].textContent;
            headerArr.push(header);

            bodyText = y[0].children[entryNum].children[1].textContent;
            bodyTextArr.push(bodyText);
            console.log(header, bodyText);
        }

        return [headerArr, bodyTextArr];
    """)

    headerArr = unformattedGameInfoStats[0]
    valuesArr = unformattedGameInfoStats[1]

    # dynamic variable detection
    cointossValueIndex = headerArr.index("Won Toss")
    cointossVal = valuesArr[cointossValueIndex]

    roofValueIndex = headerArr.index("Roof")
    roofVal = valuesArr[roofValueIndex]

    surfaceValueIndex = headerArr.index("Surface")
    surfaceVal = valuesArr[surfaceValueIndex]

    durationValueIndex = headerArr.index("Duration")
    durationVal = valuesArr[durationValueIndex]

    attendanceValueIndex = headerArr.index("Attendance")
    attendanceVal = valuesArr[attendanceValueIndex]

    weatherValueIndex = headerArr.index("Weather")
    weatherVal = valuesArr[weatherValueIndex].split(',')

    mlineValueIndex = headerArr.index("Vegas Line")
    mlineVal = valuesArr[mlineValueIndex]

    ouValueIndex = headerArr.index("Over/Under")
    ouVal = valuesArr[ouValueIndex][0:5]

    return [cointossVal, roofVal, surfaceVal, durationVal, attendanceVal, weatherVal, mlineVal, ouVal]


def convertTablesToCSVsToScrape(driver, link):
    # demo link: "https://www.pro-football-reference.com/boxscores/202310220chi.htm"
    driver.get(link)
    ### zooming out causes issue finding translated location of elements
    # driver.execute_script("document.body.style.zoom='95%'")



    def scrollAndConvertTablesToCSVs(dropdownXPATH: str, convertButtonXPATH: str, pixelsPerScroll: int = 500):
        """Continually scrolls until it finds the target elements for table to csv conversions"""
        elementInView = False
        while not elementInView:
            try: #if element can be found, extract info
                e1 = driver.find_element(By.XPATH, dropdownXPATH)
                e2 = driver.find_element(By.XPATH, convertButtonXPATH)
                action = ActionChains(driver)
                time.sleep(1)
                action.move_to_element(e1).perform()
                time.sleep(1)
                action.move_to_element(e2).click().perform()
                time.sleep(1)

                # end loop
                elementInView = True
                driver.execute_script("window.scrollBy(0, 250)")

            except Exception as e: #attempt to scroll element into view
                logging.info("Not In View, Scrolling")
                driver.execute_script("window.scrollBy(0, " + str(pixelsPerScroll) + ")")

    logging.info("--Preparing Game Tables for Scrapping--")

    ### TEAM STATS
    logging.info("Beginning Team Stats")
    teamStatsDrowdownXPATH = '/html/body/div[2]/div[5]/div[10]/div[1]/div/ul/li/span'
    teamStatsDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[10]/div[1]/div/ul/li/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(teamStatsDrowdownXPATH, teamStatsDrowdownCSVButtonXPATH)

    ### PLAYER OFF STATS
    logging.info("Beginning Offensive Stats")
    offDrowdownXPATH = '/html/body/div[2]/div[5]/div[12]/div[1]/div/ul/li[1]/span'
    offDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[12]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(offDrowdownXPATH, offDrowdownCSVButtonXPATH)

    ### PLAYER DEF STATS
    logging.info("Beginning Defensive Stats")
    defDrowdownXPATH = '/html/body/div[2]/div[5]/div[13]/div[1]/div/ul/li[1]/span'
    defDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[13]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(defDrowdownXPATH, defDrowdownCSVButtonXPATH)

    ### PLAYER Kick/Punt Returns
    logging.info("Beginning Kick Punt Return Stats")
    kprDrowdownXPATH = '/html/body/div[2]/div[5]/div[14]/div[1]/div/ul/li[1]/span'
    kprDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[14]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(kprDrowdownXPATH, kprDrowdownCSVButtonXPATH)

    ### PLAYER Kicking & Punting
    logging.info("Beginning Kick Punt Stats")
    kpDrowdownXPATH = '/html/body/div[2]/div[5]/div[16]/div[1]/div/ul/li[1]/span'
    kpDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[16]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(kpDrowdownXPATH, kpDrowdownCSVButtonXPATH)

    ### PLAYER Advanced Passing
    logging.info("Beginning Advanced Passing Stats")
    advPasDrowdownXPATH = '/html/body/div[2]/div[5]/div[17]/div[1]/div/ul/li[1]/span'
    advPasDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[17]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(advPasDrowdownXPATH, advPasDrowdownCSVButtonXPATH)

    ### PLAYER Advanced Rushing
    logging.info("Beginning Advanced Rushing Stats")
    advRusDrowdownXPATH = '/html/body/div[2]/div[5]/div[18]/div[1]/div/ul/li[1]/span'
    advRusDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[18]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(advRusDrowdownXPATH, advRusDrowdownCSVButtonXPATH)

    ### PLAYER Advanced Receiving
    logging.info("Beginning Advanced Receiving Stats")
    advRecDrowdownXPATH = '/html/body/div[2]/div[5]/div[19]/div[1]/div/ul/li[1]/span'
    advRecDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[19]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(advRecDrowdownXPATH, advRecDrowdownCSVButtonXPATH)

    ### PLAYER Advanced Defense
    logging.info("Beginning Advanced Defensive Stats")
    advRecDrowdownXPATH = '/html/body/div[2]/div[5]/div[20]/div[1]/div/ul/li[1]/span'
    advRecDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[20]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(advRecDrowdownXPATH, advRecDrowdownCSVButtonXPATH)


    ### PLAYER HOME Snap Counts
    logging.info("Beginning Home Snap Count Stats")
    hscDrowdownXPATH = '/html/body/div[2]/div[5]/div[22]/div[1]/div/div[1]/div/ul/li[1]/span'
    hscDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[22]/div[1]/div/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(hscDrowdownXPATH, hscDrowdownCSVButtonXPATH)


    ### PLAYER AWAY Snap Counts
    logging.info("Beginning Away Snap Count Stats")
    ascDrowdownXPATH = '/html/body/div[2]/div[5]/div[22]/div[2]/div/div[1]/div/ul/li[1]/span'
    ascDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[22]/div[2]/div/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(ascDrowdownXPATH, ascDrowdownCSVButtonXPATH)

    logging.info("--Game Table Transformation for Scrapping COMPLETE--")


def scrapeAllConvertedTables(driver):
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    
    ### GAME INFO
    time.sleep(3)
    gameInfoArr = scrapeGameInfo(driver)
    print(gameInfoArr)

    # get html after scrolling is complete
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    ### TEAM STATS
    crude = str(soup.find('pre', id='csv_team_stats'))
    teamStatsDF = parseScrapedCSVFormatToDF(crude)
    print(teamStatsDF)


    # ### PLAYER OFF STATS
    # crude = str(soup.find('pre', id='csv_player_offense'))
    # simpleOffStats = parseScrapedCSVFormatToDF(crude)
    # print(simpleOffStats)

    ### PLAYER DEF STATS
    crude = str(soup.find('pre', id='csv_player_defense'))
    simpleDefStats = parseScrapedCSVFormatToDF(crude)
    print(simpleDefStats)

    ### PLAYER Kick/Punt Returns
    crude = str(soup.find('pre', id='csv_returns'))
    KickPuntStats = parseScrapedCSVFormatToDF(crude)
    print(KickPuntStats)

    ### PLAYER Kicking & Punting
    crude = str(soup.find('pre', id='csv_kicking'))
    KPReturnStats = parseScrapedCSVFormatToDF(crude)
    print(KPReturnStats)

    ### PLAYER Advanced Passing
    crude = str(soup.find('pre', id='csv_passing_advanced'))
    advPassStats = parseScrapedCSVFormatToDF(crude)
    print(advPassStats)

    ### PLAYER Advanced Rushing
    crude = str(soup.find('pre', id='csv_rushing_advanced'))
    advRushStats = parseScrapedCSVFormatToDF(crude)
    print(advRushStats)

    ### PLAYER Advanced Receiving
    crude = str(soup.find('pre', id='csv_receiving_advanced'))
    advRecStats = parseScrapedCSVFormatToDF(crude)
    print(advRecStats)

    ### PLAYER Advanced Defense
    crude = str(soup.find('pre', id='csv_defense_advanced'))
    advDefStats = parseScrapedCSVFormatToDF(crude)
    print(advDefStats)

    ### PLAYER HOME Snap Counts
    crude = str(soup.find('pre', id='csv_home_snap_counts'))
    homeSnapCounts = parseScrapedCSVFormatToDF(crude)
    print(homeSnapCounts)

    ### PLAYER AWAY Snap Counts
    crude = str(soup.find('pre', id='csv_vis_snap_counts'))
    awaySnapCounts = parseScrapedCSVFormatToDF(crude)
    print(awaySnapCounts)

    ### STARTERS - TODO not yet implemented, if needed
    ### DRIVES - TODO not yet implemented, if needed
    ### PLAY-BY-PLAY - TODO not yet implemented, if needed


    return [gameInfoArr, teamStatsDF, simpleDefStats, KickPuntStats, KPReturnStats, advPassStats, advRushStats,
            advRecStats, advDefStats, homeSnapCounts, awaySnapCounts]



def gameDataScrappingManager():
    dotenv.load_dotenv()
    absProjectPath = os.getenv("ABS_PROJECT_PATH")

    # get completed game links from schedule data
    scheduleDataDF = getFinalScheduleTrainingData("2018-06-01", "2023-10-24")[1]

    # TODO: only scrape games not already recorded in /data/games/gamesData.csv
    # savedGamesPath = absProjectPath + 'data/raw/games.csv'
    # savedGamesIDArr = list(pd.read_csv(savedGamesPath).to_numpy())[0]

    seasons = scheduleDataDF['season']
    weeks = scheduleDataDF['weekNum']
    homeTeamInt = scheduleDataDF['homeFranchiseInt']
    awayTeamInt = scheduleDataDF['awayFranchiseInt']
    links = scheduleDataDF["gameLink"]

    for indexNum in range(0, len(links)):
        thisLink = links[indexNum]
        thisSeason = seasons[indexNum]
        thisWeek = weeks[indexNum]
        thisAwayTeamInt = awayTeamInt[indexNum]
        thisHomeTeamInt = homeTeamInt[indexNum]

        # create custom game identifier
        thisGameID = str(thisSeason) + "-" + str(thisWeek) + "-" + str(thisAwayTeamInt) + "-" + str(thisHomeTeamInt)

        # # check if game data exists for custom game identifier
        # if thisGameID in savedGamesIDs:
        #     continue

        # scrape away
        # else:
        # initiate driver
        thisDriver = createChromeDriver()

        # scroll through page and convert all tables to csv data to be scraped
        convertTablesToCSVsToScrape(thisDriver, thisLink)

        # read html and parse table data for each converted table
        allNestedData = scrapeAllConvertedTables(thisDriver)

        # format game data for initial storage
        formattedGameData = formatAllNestedDataForGameRecordsStorage(allNestedData, thisGameID)

        ### read all saved game data
        gamesRawDataPath = absProjectPath + 'data/raw/gamesRaw.csv'
        existingGameDataArr = pd.read_csv(gamesRawDataPath).to_numpy().tolist()
        existingGameDataArr.append(formattedGameData)# add new data entry to game data
        pd.DataFrame(existingGameDataArr, columns=gamesDataColumns).to_csv(gamesRawDataPath, index=False)

        ### format player data for initial storage
        formattedPlayersData = formatAllNestedDataForPlayersRecordsStorage(allNestedData)

        # write player data to 'data/player/raw/' + str(thisGameID) + '.csv'
        pd.DataFrame(formattedPlayersData, columns=playersDataColumns).to_csv(absProjectPath + 'data/player/raw/' + str(thisGameID) + '.csv', index=False)


    exit()











gameDataScrappingManager()