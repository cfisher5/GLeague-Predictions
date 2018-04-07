import requests
import os
import json
import pandas as pd


wd = os.getcwd()

if wd == "/home/cfisher5":
    csv_filename = "GLeaguePredictions/GLeague-Predictions/data/nba_player_data.csv"
    per_36 = "GLeaguePredictions/GLeague-Predictions/data/nba36.csv"
    merge_filename = "GLeaguePredictions/GLeague-Predictions/data/nba_merge.csv"
    nba_data = "GLeaguePredictions/GLeague-Predictions/data/nba_player_data.csv"

else:
    csv_filename = "data/nba_player_data.csv"
    per_36 = "data/nba36.csv"
    merge_filename = "data/nba_merge.csv"
    nba_data = "data/nba_player_data.csv"


def scrape():

    nba_data = open(csv_filename, 'w')
    nba_data.write('ID,height,height_inches,weight,pos\n')
    url = "http://www.nba.com/players/active_players.json"
    try:
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                    'Dnt': '1',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'en',
                    'origin': 'http://stats.nba.com'}
        response = requests.get(url, headers=header, timeout=10)
        data = response.json()
    except json.JSONDecodeError:
        print("unable to reach API")
        os.remove(csv_filename)
        return False

    for row in data:
        id = str(row['personId'])
        height = str(row['heightFeet']) + "-" + str(row['heightInches'])
        height_inches = int(row['heightFeet']) * 12 + int(row['heightInches'])
        weight = str(row['weightPounds'])
        pos = row['posExpanded']

        nba_data.write(id + "," + height + "," + str(height_inches) + "," + weight + "," + pos + "\n")

    nba_data.close()
    return True


done = False
while not done:

    done = scrape()
    data = pd.read_csv(per_36, sep=",")
    data = data[['ID', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGper', 'threeper', 'FTper']]
    height_weight_data = pd.read_csv(nba_data, sep=",")
    height_weight_data = height_weight_data[['ID', 'height_inches', 'weight']]

    merge = pd.merge(left=data, right=height_weight_data, how='inner', on='ID')
    merge.to_csv(merge_filename)
    merged = merge.drop('ID', axis=1)

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