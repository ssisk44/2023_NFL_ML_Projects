import logging
import time
import dotenv
import pandas as pd
import os
from bs4 import BeautifulSoup
from io import StringIO
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from src import constants as Constants

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

    def scrollAndConvertTablesToCSVs(dropdownXPATH: str, convertButtonXPATH: str, currentScrollAmount=300):
        """Continually scrolls until it finds the target elements for table to csv conversions"""
        elementInView = False

        while not elementInView:
            try: # attempt to find element
                e1 = driver.find_element(By.XPATH, dropdownXPATH)
                e2 = driver.find_element(By.XPATH, convertButtonXPATH)
                e1Loc = e1.location['y']

                # calculate how far I need to scroll
                scrollDistanceToElement = e1Loc - currentScrollAmount

                # scroll that far
                driver.execute_script("window.scrollBy(0," + str(scrollDistanceToElement) + ")")

                # set the ending scroll location
                currentScrollAmount = e1Loc

                action = ActionChains(driver)
                time.sleep(1)
                action.move_to_element(e1).perform()
                time.sleep(1)
                action.move_to_element(e2).click().perform()
                time.sleep(1)

                # end loop
                elementInView = True
                return currentScrollAmount

            except Exception as e: #attempt to scroll element into view
                logging.info("ERROR Pre-Scrolling while Scrapping Game")

    logging.info("--Preparing Game Tables for Scrapping--")

    ### TEAM STATS
    logging.info("Beginning Team Stats")
    teamStatsDrowdownXPATH = '/html/body/div[2]/div[5]/div[10]/div[1]/div/ul/li/span'
    teamStatsDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[10]/div[1]/div/ul/li/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(teamStatsDrowdownXPATH, teamStatsDrowdownCSVButtonXPATH)

    ### PLAYER OFF STATS
    logging.info("Beginning Offensive Stats")
    offDrowdownXPATH = '/html/body/div[2]/div[5]/div[12]/div[1]/div/ul/li[1]/span'
    offDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[12]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(offDrowdownXPATH, offDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER DEF STATS
    logging.info("Beginning Defensive Stats")
    defDrowdownXPATH = '/html/body/div[2]/div[5]/div[13]/div[1]/div/ul/li[1]/span'
    defDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[13]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(defDrowdownXPATH, defDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER Kick/Punt Returns
    logging.info("Beginning Kick Punt Return Stats")
    kprDrowdownXPATH = '/html/body/div[2]/div[5]/div[14]/div[1]/div/ul/li[1]/span'
    kprDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[14]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(kprDrowdownXPATH, kprDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER Kicking & Punting
    logging.info("Beginning Kick Punt Stats")
    kpDrowdownXPATH = '/html/body/div[2]/div[5]/div[16]/div[1]/div/ul/li[1]/span'
    kpDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[16]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(kpDrowdownXPATH, kpDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER Advanced Passing
    logging.info("Beginning Advanced Passing Stats")
    advPasDrowdownXPATH = '/html/body/div[2]/div[5]/div[17]/div[1]/div/ul/li[1]/span'
    advPasDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[17]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(advPasDrowdownXPATH, advPasDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER Advanced Rushing
    logging.info("Beginning Advanced Rushing Stats")
    advRusDrowdownXPATH = '/html/body/div[2]/div[5]/div[18]/div[1]/div/ul/li[1]/span'
    advRusDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[18]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(advRusDrowdownXPATH, advRusDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER Advanced Receiving
    logging.info("Beginning Advanced Receiving Stats")
    advRecDrowdownXPATH = '/html/body/div[2]/div[5]/div[19]/div[1]/div/ul/li[1]/span'
    advRecDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[19]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(advRecDrowdownXPATH, advRecDrowdownCSVButtonXPATH, currentScrollAmount)

    ### PLAYER Advanced Defense
    logging.info("Beginning Advanced Defensive Stats")
    advRecDrowdownXPATH = '/html/body/div[2]/div[5]/div[20]/div[1]/div/ul/li[1]/span'
    advRecDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[20]/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(advRecDrowdownXPATH, advRecDrowdownCSVButtonXPATH, currentScrollAmount)


    ### PLAYER HOME Snap Counts
    logging.info("Beginning Home Snap Count Stats")
    hscDrowdownXPATH = '/html/body/div[2]/div[5]/div[22]/div[1]/div/div[1]/div/ul/li[1]/span'
    hscDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[22]/div[1]/div/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    currentScrollAmount = scrollAndConvertTablesToCSVs(hscDrowdownXPATH, hscDrowdownCSVButtonXPATH, currentScrollAmount)


    ### PLAYER AWAY Snap Counts
    logging.info("Beginning Away Snap Count Stats")
    ascDrowdownXPATH = '/html/body/div[2]/div[5]/div[22]/div[2]/div/div[1]/div/ul/li[1]/span'
    ascDrowdownCSVButtonXPATH = '/html/body/div[2]/div[5]/div[22]/div[2]/div/div[1]/div/ul/li[1]/div/ul/li[3]/button'
    scrollAndConvertTablesToCSVs(ascDrowdownXPATH, ascDrowdownCSVButtonXPATH, currentScrollAmount)

    logging.info("--Game Table Transformation for Scrapping COMPLETE--")


def scrapeAllConvertedTables(driver, saveToTemp=False):
    absProjectFilepath = os.getenv("ABS_PROJECT_PATH")
    
    ### GAME INFO
    time.sleep(3)
    gameInfoArr = scrapeGameInfo(driver)

    # get html after scrolling is complete
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    ### TEAM STATS
    crude = str(soup.find('pre', id='csv_team_stats'))
    teamStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER OFF STATS
    crude = str(soup.find('pre', id='csv_player_offense'))
    simpleOffStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER DEF STATS
    crude = str(soup.find('pre', id='csv_player_defense'))
    simpleDefStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER Kick/Punt Returns
    crude = str(soup.find('pre', id='csv_returns'))
    kPReturnStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER Kicking & Punting
    crude = str(soup.find('pre', id='csv_kicking'))
    kickPuntStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER Advanced Passing
    crude = str(soup.find('pre', id='csv_passing_advanced'))
    advPassStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER Advanced Rushing
    crude = str(soup.find('pre', id='csv_rushing_advanced'))
    advRushStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER Advanced Receiving
    crude = str(soup.find('pre', id='csv_receiving_advanced'))
    advRecStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER Advanced Defense
    crude = str(soup.find('pre', id='csv_defense_advanced'))
    advDefStatsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER HOME Snap Counts
    crude = str(soup.find('pre', id='csv_home_snap_counts'))
    homeSnapCountsDF = parseScrapedCSVFormatToDF(crude)

    ### PLAYER AWAY Snap Counts
    crude = str(soup.find('pre', id='csv_vis_snap_counts'))
    awaySnapCountsDF = parseScrapedCSVFormatToDF(crude)


    ### STARTERS - TODO not yet implemented, if needed
    ### DRIVES - TODO not yet implemented, if needed
    ### PLAY-BY-PLAY - TODO not yet implemented, if needed

    if saveToTemp:
        pd.DataFrame(gameInfoArr, index=None).to_csv(absProjectFilepath + "tmp/gameInfo.csv", header=True)
        teamStatsDF.to_csv(absProjectFilepath + "tmp/teamStatsDF.csv")
        simpleOffStatsDF.to_csv(absProjectFilepath + "tmp/simpleOffStatsDF.csv", header=False)
        simpleDefStatsDF.to_csv(absProjectFilepath + "tmp/simpleDefStatsDF.csv", header=False)
        kickPuntStatsDF.to_csv(absProjectFilepath + "tmp/kickPuntStatsDF.csv", header=False)
        kPReturnStatsDF.to_csv(absProjectFilepath + "tmp/kPReturnStatsDF.csv", header=False)
        advPassStatsDF.to_csv(absProjectFilepath + "tmp/advPassStatsDF.csv", header=True)
        advRushStatsDF.to_csv(absProjectFilepath + "tmp/advRushStatsDF.csv", header=True)
        advRecStatsDF.to_csv(absProjectFilepath + "tmp/advRecStatsDF.csv", header=True)
        advDefStatsDF.to_csv(absProjectFilepath + "tmp/advDefStatsDF.csv", header=True)
        homeSnapCountsDF.columns = Constants.snapCountDataColumns
        homeSnapCountsDF.to_csv(absProjectFilepath + "tmp/homeSnapCountsDF.csv", header=False)
        awaySnapCountsDF.columns = Constants.snapCountDataColumns
        awaySnapCountsDF.to_csv(absProjectFilepath + "tmp/awaySnapCountsDF.csv", header=False)


    # return [gameInfoArr, teamStatsDF, simpleDefStatsDF, kickPuntStatsDF, kPReturnStatsDF, advPassStatsDF, advRushStatsDF,
    #         advRecStatsDF, advDefStatsDF, homeSnapCountsDF, awaySnapCountsDF]


def gameDataScrappingManager(beginningSeasonRangeInt, endingSeasonRangeInt):
    absProjectPath = os.getenv("ABS_PROJECT_PATH")

    # get completed game links from schedule data
    scheduleDataDF = pd.read_csv(absProjectPath + 'data/schedule/NFL-Historical-Schedule-And-Results.csv')

    # initialize new Chrome Driver
    thisDriver = createChromeDriver()

    gameIDs = scheduleDataDF['gameID']
    seasons = scheduleDataDF['gameSeason']
    weeks = scheduleDataDF['gameWeek']
    links = scheduleDataDF["gameLink"]

    for indexNum in range(0, len(links)):
        thisGameID = gameIDs[indexNum]
        thisSeason = seasons[indexNum]
        thisWeek = weeks[indexNum]
        thisLink = links[indexNum]

        ### make sure the desired game to scrape is within the range parameters
        if not (beginningSeasonRangeInt <= int(thisSeason) <= endingSeasonRangeInt):
            logging.info("Skipping " + str(thisSeason) + " " + str(thisWeek) + ". Not in the desired range of " + str(beginningSeasonRangeInt) + " to " + str(endingSeasonRangeInt))
            continue


        # ### TODO: check if transformed game data in records so you can skip the game
        # gamesRawDataPath = absProjectPath + 'data/gameData/gamesInfoData.csv'
        # existingGameDataDF = pd.read_csv(gamesRawDataPath)
        # existingGameIDs = existingGameDataDF['gameID']
        # if thisGameID in existingGameIDs:
        #     logging.info("Skipping " + str(thisGameID))
        #     continue


        # scroll through page and convert all tables to csv data to be scraped
        convertTablesToCSVsToScrape(thisDriver, thisLink)

        # read html and parse table data for each converted table
        allNestedData = scrapeAllConvertedTables(thisDriver, True)


        exit()

        ### collect game data
        ### write game data record to gameInfoData.csv

        ### collect player data
        ### write playerData to gamePlayerData.csv



        # # write player data to 'data/player/raw/' + str(thisGameID) + '.csv'
        # pd.DataFrame(formattedPlayersData, columns=playersDataColumns).to_csv(absProjectPath + 'data/player/raw/' + str(thisGameID) + '.csv', index=False)


    exit()

