import requests
import os
import csv
import json
import global_items


def scrape():
    wd = os.getcwd()

    if wd == "/home/cfisher5":
        pace_csv = "GLeague-Predictions/data/pace.csv"
        nba_per_36 = "GLeague-Predictions/data/nba36.csv"
        per36_json = "GLeague-Predictions/data/nbaper36.json"
    else:
        nba_per_36 = "data/nba36.csv"
        per36_json = "data/nbaper36.json"
        pace_csv = "data/pace.csv"

    avg_pace = None
    with open(pace_csv, "r") as pace_file:
        pace = csv.reader(pace_file)
        next(pace, None)
        for team in pace:
            if team[0] == "avg":
                avg_pace = float(team[1])
                break

    nba_36 = open(nba_per_36, "w")
    nba_36.write('index,ID,Name,TeamID,Team,GP,TotalMin,PTS,REB,AST,STL,BLK,TOV,FGper,threeper,FTper\n')

    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
          "&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&" \
          "MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=0" \
          "&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=" \
          "&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        response = requests.get(url, headers=global_items.header, timeout=100)
        data = response.json()['resultSets'][0]['rowSet']
        print("using API")
    except requests.ReadTimeout:
        print("unable to reach API, so using old json")
        data = json.load(open(per36_json))['resultSets'][0]['rowSet']

    index = 0
    print("grabbing nba per 36")

    for row in data:
        min = row[9]
        if min < 300:
            continue
        id = str(row[0])
        name = str(row[1])
        teamID = str(row[2])
        team = str(row[3])
        with open(pace_csv, 'r') as pace_file:
            rows = csv.reader(pace_file, delimiter=",")
            next(rows, None)
            for t in rows:
                if teamID == t[0]:
                    pace = t[1]
                    break

        gp = str(row[5])
        min = str(min)
        pts = str(float(row[29]) * (avg_pace/float(pace)))
        reb = str(float(row[21]) * (avg_pace/float(pace)))
        ast = str(float(row[22]) * (avg_pace/float(pace)))
        stl = str(float(row[24]) * (avg_pace/float(pace)))
        blk = str(float(row[25]) * (avg_pace/float(pace)))
        tov = str(float(row[23]) * (avg_pace/float(pace)))
        fgper = str(float(row[12]) * (avg_pace/float(pace)))
        threeper = str(float(row[15]) * (avg_pace/float(pace)))
        ftper = str(float(row[18]) * (avg_pace/float(pace)))

        nba_36.write(str(index) + "," + id + "," + name + "," + teamID + "," + team + "," + gp + "," + min + "," + pts+ "," + reb + "," +
                     ast + "," + stl + "," + blk + "," + tov + "," + fgper + "," + threeper + "," + ftper + "\n")
        index += 1
    nba_36.close()

    return True


done = False
while not done:
    done = scrape()
