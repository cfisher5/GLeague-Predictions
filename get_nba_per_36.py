import requests
import os
import csv


def scrape():

    avg_pace = None
    with open("data/pace.csv", "r") as pace_file:
        pace = csv.reader(pace_file)
        next(pace, None)
        for team in pace:
            if team[0] == "avg":
                avg_pace = float(team[1])
                break

    wd = os.getcwd()
    if wd == "/home/cfisher5":
        nba_per_36 = "GLeaguePredictions/GLeague-Predictions/data/nba36.csv"
    else:
        nba_per_36 = "data/nba36.csv"

    nba_36 = open(nba_per_36, 'w')
    nba_36.write('index,ID,Name,TeamID,Team,GP,TotalMin,PTS,REB,AST,STL,BLK,TOV,FGper,threeper,FTper\n')

    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
          "&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&" \
          "MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=0" \
          "&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=" \
          "&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Dnt': '1',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en',
            'origin': 'http://stats.nba.com'}
        response = requests.get(url, headers=header, timeout=10)
        data = response.json()['resultSets'][0]['rowSet']
    except requests.ReadTimeout:
        print("unable to reach API")
        return False
    index = 0
    print("grabbing nba per 36")
    for row in data:
        min = row[9]
        if min < 300:
            print("did not pass min threshold of 300 min")
            continue
        id = str(row[0])
        name = str(row[1])
        teamID = str(row[2])
        team = str(row[3])
        with open("data/pace.csv", 'r') as pace_file:
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

