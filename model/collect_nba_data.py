import json
import random

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time


def scrape(json, stat_type, season, headers=None):
    try:
        if stat_type == "shooting":
            data = json['resultSets']['rowSet']
        else:
            data = json['resultSets'][0]['rowSet']

        if headers is None:
            headers = json['resultSets'][0]['headers']
        df = pd.DataFrame(data, columns=headers)
        df_filename = "data/nba/nba_" + stat_type + "_" + season + ".csv"
        df.to_csv(df_filename, index=False)
    except json.JSONDecodeError:
        print("unable to reach API")


def get_json_from_api(url):
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-logging")
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(8)

    try:
        driver.get(url)
        time.sleep(random.randint(3, 11))
    except TimeoutException:
        driver.execute_script("window.stop();")
        print("window stopped")

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    string = soup.find("pre").text
    json_text = json.loads(string)
    driver.quit()
    return json_text


years = ["2007-08", "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16","2016-17", "2017-18"]

for season in years:

    print(season)

    print("per36")
    # get per36 stats
    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    json_text = get_json_from_api(url)
    scrape(json_text, "per36", season)

    print("advanced")
    # get advanced stats
    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    json_text = get_json_from_api(url)
    scrape(json_text, "advanced", season)

    print("usage")
    # get usage stats
    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Usage&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    json_text = get_json_from_api(url)
    scrape(json_text, "usage", season)

    print("scoring")
    # get scoring stats
    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Scoring&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    json_text = get_json_from_api(url)
    scrape(json_text, "scoring", season)

    print("shooting")
    # get shooting stats
    url = "http://stats.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=By+Zone&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    headers = ["PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_ABBREVIATION","AGE","RA_FGM","RA_FGA","RA_FG_PCT","Paint_FGM","Paint_FGA","Paint_FG_PCT","Mid-Range_FGM","Mid-Range_FGA","Mid-Range_FG_PCT","Left_Corner_FGM","Left_Corner_FGA","Left_Corner_FG_PCT","Right_Corner_FGM","Right_Corner_FGA","Right_Corner_FG_PCT","Above_Break_FGM","Above_Break_FGA","Above_Break_FG_PCT","Backcourt_FGM","Backcourt_FGA","Backcourt_FG_PCT"]
    json_text = get_json_from_api(url)
    scrape(json_text, "shooting", season, headers=headers)


