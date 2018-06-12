import requests
import json
import pandas as pd

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'connection': 'keep-alive',
    "accept-encoding": "Accepflate, sdch",
    'accept-language': 'he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4',
    }


def scrape(url, stat_type, season, headers=None):
    try:
        response = requests.get(url, headers=header, timeout=500)

        if stat_type == "shooting":
            data = response.json()['resultSets']['rowSet']
        else:
            data = response.json()['resultSets'][0]['rowSet']

        if headers is None:
            headers = response.json()['resultSets'][0]['headers']
        df = pd.DataFrame(data, columns=headers)
        df_filename = "data/gleague/gleague_" + stat_type + "_" + season + ".csv"
        df.to_csv(df_filename, index=False)
    except json.JSONDecodeError:
        print("unable to reach API")


years = ["2007-08", "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16","2016-17", "2017-18"]

for season in years:

    print(season)
    # get per36 stats
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=" \
          "&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=" \
          "&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0" \
          "&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=" \
          "0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=" \
          "&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    scrape(url, "per36", season)

    #get advanced stats
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
          "&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Advanced" \
          "&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=Y&PerMode=Totals&Period=0&PlayerExperience=" \
          "&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=" \
          "&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    scrape(url, "advanced", season)

    #get usage stats
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
          "&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Usage" \
          "&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&" \
          "PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=" \
          "&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight"
    scrape(url, "usage", season)

    #get scoring stats
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=" \
          "&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Scoring&Month=0" \
          "&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=" \
          "&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&" \
          "TeamID=0&VsConference=&VsDivision=&Weight="
    scrape(url, "scoring", season)

    #get shooting stats
    url = "http://stats.gleague.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=" \
          "&DateTo=&DistanceRange=By+Zone&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20" \
          "&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0" \
          "&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=" + season + "&SeasonSegment=&SeasonType=Regular+Season" \
          "&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    headers = ["PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_ABBREVIATION","AGE","RA_FGM","RA_FGA","RA_FG_PCT","Paint_FGM","Paint_FGA","Paint_FG_PCT","Mid-Range_FGM","Mid-Range_FGA","Mid-Range_FG_PCT","Left_Corner_FGM","Left_Corner_FGA","Left_Corner_FG_PCT","Right_Corner_FGM","Right_Corner_FGA","Right_Corner_FG_PCT","Above_Break_FGM","Above_Break_FGA","Above_Break_FG_PCT","Backcourt_FGM","Backcourt_FGA","Backcourt_FG_PCT"]
    scrape(url, "shooting", season, headers=headers)


