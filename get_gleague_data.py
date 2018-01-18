import requests
import os
import json
from fake_useragent import UserAgent


player_json = []
wd = os.getcwd()
print(wd)

if wd == "/home/cfisher5":
    csv_filename = "GLeaguePredictions/GLeague-Predictions/data/gleague_data_new.csv"
    json_filename = "GLeaguePredictions/GLeague-Predictions/data/players_json_new.txt"
    old_csv_filename = "GLeaguePredictions/GLeague-Predictions/data/gleague_data.csv"
    old_json_filename = "GLeaguePredictions/GLeague-Predictions/data/players_json.txt"
else:
    csv_filename = "data/gleague_data_new.csv"
    json_filename = "data/players_json_new.txt"
    old_csv_filename = "data/gleague_data.csv"
    old_json_filename = "data/players_json.txt"

gleague_ids = open(csv_filename, 'w')
gleague_ids.write('Name,ID,Team,Age,GP,FGA,3PM,REB,AST,PTS\n')

url = "http://stats.gleague.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=20&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

try:
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)}
    print(header)
    response = requests.get(url, headers=header)
    print(response)
    data = response.json()['resultSets'][0]['rowSet']
except json.JSONDecodeError:
    print("unable to reach API")
    os.remove(csv_filename)
    exit(1)

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

players_file = open(json_filename, 'w')
players_file.write(str(player_json))
players_file.close()

my_domain = 'www.gleaguetonba.com'
username = 'cfisher5'
token = 'a844de4d08ca51a979b47c54e80acea23a434b8e'

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/'.format(
        username=username, domain=my_domain
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('All OK')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))


os.remove(old_csv_filename)
os.remove(old_json_filename)

os.rename(csv_filename, old_csv_filename)
os.rename(json_filename, old_json_filename)
