import requests
import os
import json
import time
import global_items
import pandas as pd


def scrape():
    player_json = []
    wd = os.getcwd()

    if wd == "/home/cfisher5":
        csv_filename = "GLeague-Predictions/data/gleague_data_new.csv"
        json_filename = "GLeague-Predictions/data/players_json_new.txt"
        old_csv_filename = "GLeague-Predictions/data/gleague_data.csv"
        old_json_filename = "GLeague-Predictions/data/players_json.txt"
        gleague_projections_csv = "GLeague-Predictions/data/gleague_projections.csv"
        pace_json = "GLeague-Predictions/data/pace.json"
        pace_csv = "GLeague-Predictions/data/pace.csv"
        advanced_csv = "GLeague-Predictions/data/gleague_advanced.csv"
        shooting_csv = "GLeague-Predictions/data/shooting.csv"
        min_csv = "GLeague-Predictions/data/min.csv"
        usage_csv = "GLeague-Predictions/data/usage.csv"

    else:
        csv_filename = "data/gleague_data_new.csv"
        json_filename = "data/players_json_new.txt"
        old_csv_filename = "data/gleague_data.csv"
        old_json_filename = "data/players_json.txt"
        gleague_projections_csv = "data/gleague_projections.csv"
        pace_csv = "data/pace.csv"
        pace_json = "data/pace.json"
        advanced_csv = "data/gleague_advanced.csv"
        shooting_csv = "data/shooting.csv"
        min_csv = "data/min.csv"
        usage_csv = "data/usage.csv"

    #gleague total min
    print("grabbing total min")
    totals_url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        response = requests.get(totals_url, headers=global_items.header, timeout=1000)
        totals_data = response.json()['resultSets'][0]['rowSet']
        headers = response.json()['resultSets'][0]['headers']
    except json.JSONDecodeError:
        print("unable to reach API")
        return False

    df = pd.DataFrame(totals_data, columns=headers)
    df = df[['PLAYER_ID', 'MIN']]
    df.to_csv(min_csv, index=False)

    # gleague box score data
    gleague_ids = open(csv_filename, 'w')
    gleague_ids.write('Name,ID,Team,Age,GP,FGA,3PM,REB,AST,PTS,MIN,FGM,FGP,3PA,3PPER,FTM,FTA,FTPER,TOV,STL,BLK\n')
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        response = requests.get(url, headers=global_items.header, timeout=1000)
        data = response.json()['resultSets'][0]['rowSet']
    except json.JSONDecodeError:
        print("unable to reach API")
        os.remove(csv_filename)
        return False

    print("grabbing g league box score data")
    for obj in data:
        player = {}
        name = obj[1]
        href = str(obj[0])
        team = str(obj[3])
        age = str(obj[4]).replace(".0", "")
        gp = str(obj[5])
        minutes = str(obj[9])
        fgm = str(obj[10])
        fga = str(obj[11])
        fgper = str(obj[12])
        threepm = str(obj[13])
        threepa = str(obj[14])
        threeper = str(obj[15])
        ftm = str(obj[16])
        fta = str(obj[17])
        ftper = str(obj[18])
        reb = str(obj[21])
        ast = str(obj[22])
        tov = str(obj[23])
        stl = str(obj[24])
        blk = str(obj[25])
        pts = str(obj[29])

        player["label"] = name
        player["value"] = href

        if player_json.__contains__(player):
            print("ALREADY INSIDE")
            continue

        else:
            player_json.append(player)

        gleague_ids.write(name + "," + href + "," + team + "," + age + "," + gp + "," + fga + "," + threepm + "," + reb + "," + ast + "," + pts + ',' + minutes + "," + fgm + "," + fgper + "," + threepa + "," + threeper + "," + ftm + "," + fta + "," + ftper + "," + tov + "," + stl + "," + blk + "\n")

    gleague_ids.close()
    players_file = open(json_filename, 'w')
    players_file.write(str(player_json))
    players_file.close()

    # gleague advanced stats
    gleague_adv = open(advanced_csv, 'w')
    gleague_adv.write('ID,GP,ORTG,DRTG,NRTG,ASTPER,OREBPER,DREBPER,eFG,TS,USG\n')
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        response = requests.get(url, headers=global_items.header, timeout=1000)
        data = response.json()['resultSets'][0]['rowSet']
    except json.JSONDecodeError:
        print("unable to reach API")
        return False

    print("grabbing g league advanced data")
    for player in data:
        player_id = player[0]
        gp = player[5]
        ortg = player[10]
        drtg = player[11]
        nrtg = player[12]
        astper = player[13]
        orebper = player[16]
        drebper = player[17]
        efg = player[20]
        ts = player[21]
        usg = player[22]

        gleague_adv.write(str(player_id) + "," + str(gp) + "," + str(ortg)+ "," + str(drtg)+ "," + str(nrtg) + ","
                          + str(astper) + "," + str(orebper) + "," +str(drebper) +
                          "," + str(efg) + "," + str(ts) + "," + str(usg) + "\n")

    gleague_adv.close()
    time.sleep(5)


    #getting shots
    print("grabbing shot location data")
    shots_url = "http://stats.gleague.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=By+Zone&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    headers = ["PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_ABBREVIATION","AGE","RA_FGM","RA_FGA","RA_FG_PCT","Paint_FGM","Paint_FGA","Paint_FG_PCT","Mid-Range_FGM","Mid-Range_FGA","Mid-Range_FG_PCT","Left_Corner_FGM","Left_Corner_FGA","Left_Corner_FG_PCT","Right_Corner_FGM","Right_Corner_FGA","Right_Corner_FG_PCT","Above_Break_FGM","Above_Break_FGA","Above_Break_FG_PCT","Backcourt_FGM","Backcourt_FGA","Backcourt_FG_PCT"]

    try:
        response = requests.get(shots_url, headers=global_items.header, timeout=1000)
        shot_data = response.json()['resultSets']['rowSet']
    except json.JSONDecodeError:
        print("unable to reach API")
        return False

    df = pd.DataFrame(shot_data, columns=headers)
    df.to_csv(shooting_csv, index=False)

    # getting usage stats
    print("grabbing usage data")
    usg_url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Usage&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    try:
        response = requests.get(usg_url, headers=global_items.header, timeout=1000)
        headers = response.json()['resultSets'][0]['headers']
        usg_data = response.json()['resultSets'][0]['rowSet']
    except json.JSONDecodeError:
        print("unable to reach API")
        return False

    df = pd.DataFrame(usg_data, columns=headers)
    df.to_csv(usage_csv, index=False)

    # gleague nba projections
    gleague_projections = open(gleague_projections_csv, 'w')
    gleague_projections.write('ID,PTS,REB,AST,STL,BLK,TOV,FGper,threeper,FTper\n')
    proj_url = "http://stats.gleague.nba.com/stats/dleaguepredictor?DLeagueTeamID=0&LeagueID=20&NBATeamID=0&Season=2017-18"
    try:
        response = requests.get(proj_url, headers=global_items.header, timeout=1000)
        proj_data = response.json()['resultSets'][0]['rowSet']
    except json.JSONDecodeError:
        print("unable to reach API")
        return False

    print("grabbing g league -> nba projection data")
    for row in proj_data:
        id = str(row[0])
        PTS = str(row[14])
        REB = str(row[15])
        AST = str(row[16])
        STL = str(row[17])
        BLK = str(row[18])
        TOV = str(row[19])
        FGper = str(row[20])
        threepper = str(row[21])
        ftper = str(row[22])

        gleague_projections.write(id + "," + PTS + "," + REB + "," + AST + "," + STL + "," + BLK + "," + TOV + "," + FGper + "," + threepper + "," + ftper + "\n" )

    gleague_projections.close()

    # NBA pace info
    pace_file = open(pace_csv, 'w')
    pace_file.write("TeamID,pace\n")
    total_pace = 0.0

    # url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision="
    # worked = False
    # while not worked:
    #     try:
    #         ua = UserAgent()
    #         random_header = ua.random
    #         print(random_header)
    #         header = {
    #             'user-agent': random_header,
    #             'Dnt': '1',
    #             'Accept-Encoding': 'gzip, deflate, sdch',
    #             'Accept-Language': 'en',
    #             'origin': 'http://stats.nba.com'}
    #         response = requests.get(url, headers=header, timeout=(5, 15))
    #         pace_data = response.json()['resultSets'][0]['rowSet']
    #         worked = True
    #     except json.JSONDecodeError:
    #         print("unable to reach API")
    #         return False
    #     except requests.exceptions.ReadTimeout:
    #         print("experiencing timeout...")

    pace_data = json.load(open(pace_json))

    print("grabbing pace information")
    for team in pace_data['resultSets'][0]['rowSet']:
        total_pace += team[19]
        pace_file.write(str(team[0]) + "," + str(team[19]) + "\n")

    avg_pace = total_pace / 30.0
    pace_file.write("avg," + str(avg_pace))
    pace_file.close()

    os.remove(old_csv_filename)
    os.remove(old_json_filename)

    os.rename(csv_filename, old_csv_filename)
    os.rename(json_filename, old_json_filename)

    return True


done = False
while not done:
    done = scrape()
