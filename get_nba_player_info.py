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
    active_json = "GLeaguePredictions/GLeague-Predictions/data/activeplayers.json"

else:
    csv_filename = "data/nba_player_data.csv"
    per_36 = "data/nba36.csv"
    merge_filename = "data/nba_merge.csv"
    nba_data = "data/nba_player_data.csv"
    active_json = "data/activeplayers.json"


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
        print("unable to reach API so using old json")
        data = json.loads(open(active_json))

    for row in data:
        id = str(row['personId'])
        height = str(row['heightFeet']) + "-" + str(row['heightInches'])
        try:
            height_inches = int(row['heightFeet']) * 12 + int(row['heightInches'])
            weight = str(row['weightPounds'])
            pos = row['posExpanded']
            nba_data.write(id + "," + height + "," + str(height_inches) + "," + weight + "," + pos + "\n")
        except ValueError:
            print("player " + id + " does not have height listed. excluding him.")
            continue

    nba_data.close()
    return True


done = scrape()
data = pd.read_csv(per_36, sep=",")
data = data[['ID', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGper', 'threeper', 'FTper']]
height_weight_data = pd.read_csv(nba_data, sep=",")
height_weight_data = height_weight_data[['ID', 'height_inches', 'weight']]

merge = pd.merge(left=data, right=height_weight_data, how='inner', on='ID')
merge.to_csv(merge_filename)
merged = merge.drop('ID', axis=1)
