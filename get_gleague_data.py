import requests
import os
import json
from fake_useragent import UserAgent
import time
import csv

def scrape():
    player_json = []
    wd = os.getcwd()

    if wd == "/home/cfisher5":
        csv_filename = "GLeaguePredictions/GLeague-Predictions/data/gleague_data_new.csv"
        json_filename = "GLeaguePredictions/GLeague-Predictions/data/players_json_new.txt"
        old_csv_filename = "GLeaguePredictions/GLeague-Predictions/data/gleague_data.csv"
        old_json_filename = "GLeaguePredictions/GLeague-Predictions/data/players_json.txt"
        gleague_projections_csv = "GLeaguePredictions/GLeague-Predictions/data/gleague_projections.csv"
        pace_csv = "GLeaguePredictions/GLeague-Predictions/data/pace.csv"
        nba_per_36 = "GLeaguePredictions/GLeague-Predictions/data/nba36.csv"
    else:
        csv_filename = "data/gleague_data_new.csv"
        json_filename = "data/players_json_new.txt"
        old_csv_filename = "data/gleague_data.csv"
        old_json_filename = "data/players_json.txt"
        gleague_projections_csv = "data/gleague_projections.csv"
        pace_csv = "data/pace.csv"
        nba_per_36 = "data/nba36.csv"


    gleague_ids = open(csv_filename, 'w')
    gleague_ids.write('Name,ID,Team,Age,GP,FGA,3PM,REB,AST,PTS\n')
    url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                    'Dnt': '1',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'en',
                    'origin': 'http://stats.nba.com'}
        response = requests.get(url, headers=header, timeout=10)
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
        fga = str(obj[11])
        threepm = str(obj[13])
        reb = str(obj[21])
        ast = str(obj[22])
        pts = str(obj[29])

        player["label"] = name
        player["value"] = href

        if player_json.__contains__(player):
            print("ALREADY INSIDE")
            continue

        else:
            player_json.append(player)

        gleague_ids.write(name + "," + href + "," + team + "," + age + "," + gp + "," + fga + "," + threepm + "," + reb + "," + ast + "," + pts + "\n")

    players_file = open(json_filename, 'w')
    players_file.write(str(player_json))
    players_file.close()

    time.sleep(5)

    gleague_projections = open(gleague_projections_csv, 'w')
    gleague_projections.write('ID,PTS,REB,AST,STL,BLK,TOV,FGper,threeper,FTper\n')
    proj_url = "http://stats.gleague.nba.com/stats/dleaguepredictor?DLeagueTeamID=0&LeagueID=20&NBATeamID=0&Season=2017-18"
    try:
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Dnt': '1',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en',
            'origin': 'http://stats.nba.com'}
        response = requests.get(proj_url, headers=header, timeout=10)
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
    # time.sleep(120)
    # get pace info
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

    pace_data = json.load(open('data/pace.json'))

    print("grabbing pace information")
    for team in pace_data['resultSets'][0]['rowSet']:
        total_pace += team[19]
        pace_file.write(str(team[0]) + "," + str(team[19]) + "\n")

    avg_pace = total_pace / 30.0
    pace_file.write("avg," + str(avg_pace))
    pace_file.close()

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
        with open(pace_csv, 'r') as pace_file:
            rows = csv.reader(pace_file, delimiter=",")
            next(rows, None)
            for t in rows:
                if teamID == t[0]:
                    pace = t[1]
                    print(team + " pace: " + pace)
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

    my_domain = 'www.gleaguetonba.com'
    username = 'cfisher5'
    token = 'a844de4d08ca51a979b47c54e80acea23a434b8e'

    response = requests.post(
        'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/'.format(
            username=username, domain=my_domain
        ),
        headers={'Authorization': 'Token {token}'.format(token=token)}, timeout=10
    )
    if response.status_code == 200:
        print('All OK')
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))

    os.remove(old_csv_filename)
    os.remove(old_json_filename)

    os.rename(csv_filename, old_csv_filename)
    os.rename(json_filename, old_json_filename)

    return True


done = False
while not done:
    done = scrape()
