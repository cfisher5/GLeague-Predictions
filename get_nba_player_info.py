import requests
import os
import json
import pandas as pd
import global_items

wd = os.getcwd()

if wd == "/home/cfisher5":
    csv_filename = "GLeague-Predictions/data/nba_player_data.csv"
    per_36 = "GLeague-Predictions/data/nba36.csv"
    merge_filename = "GLeague-Predictions/data/nba_merge.csv"
    nba_data = "GLeague-Predictions/data/nba_player_data.csv"
    active_json = "GLeague-Predictions/data/activeplayers.json"

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
        response = requests.get(url, headers=global_items.header, timeout=10)
        data = response.json()
        print("grabbing nba player measurement/position data, and saving json for next time...")
        with open(active_json, 'w') as outfile:
            json.dump(data, outfile)
            
    except requests.ReadTimeout:
        print("unable to reach API so using old json")
        data = json.load(open(active_json))

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
print(per_36)
data = pd.read_csv(open(per_36, "r"), sep=",")
print(data.head())
data = data[['ID', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGper', 'threeper', 'FTper']]
height_weight_data = pd.read_csv(nba_data, sep=",")
height_weight_data = height_weight_data[['ID', 'height_inches', 'weight']]

merge = pd.merge(left=data, right=height_weight_data, how='inner', on='ID')
merge.to_csv(merge_filename)
merged = merge.drop('ID', axis=1)
