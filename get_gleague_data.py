import requests
import os

player_json = []
print(os.getcwd())

gleague_ids = open('data/gleague_data.csv', 'w')
gleague_ids.write('Name,ID,Team,Age,GP,FGA,3PM,REB,AST,PTS\n')

url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
response = requests.get(url)
data = response.json()['resultSets'][0]['rowSet']
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

    player['label'] = name
    player['value'] = href

    if player_json.__contains__(player):
        print("ALREADY INSIDE")
        continue

    else:
        player_json.append(player)

    gleague_ids.write(name + "," + href + "," + team + "," + age + "," + gp + "," + fga + "," + threepm + "," + reb + "," + ast + "," + pts + "\n")

players_file = open('data/players_json.txt', 'w')
players_file.write(str(player_json))
players_file.close()