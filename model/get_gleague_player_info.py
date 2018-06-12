import pandas as pd
import requests
import json

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'connection': 'keep-alive',
    "accept-encoding": "Accepflate, sdch",
    'accept-language': 'he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4',
    }

years = ["2007-08", "2008-09", "2009-10", "2010-11", "2011-12", "2012-13", "2013-14", "2014-15", "2015-16","2016-17", "2017-18"]
df_array = []

for season in years:
    for stat in ['advanced', 'per36', 'scoring', 'shooting', 'usage']:
        df_to_add = pd.read_csv(filepath_or_buffer="data/gleague/gleague_" + stat + "_" + season + ".csv")
        df = df_to_add[['PLAYER_ID']]
        df_array.append(df)


all_players = pd.concat(df_array)
all_unique_players = all_players['PLAYER_ID'].unique()
list_players = sorted(all_unique_players)

# get data for each player in dataset
csv_filename = "data/player_info.csv"
csv = open(csv_filename, 'w')
csv.write('PLAYER_ID,birthday,height,weight,position,draft_year,draft_number\n')
for player_id in list_players:
    print(player_id)
    url = "http://stats.gleague.nba.com/stats/commonplayerinfo?LeagueID=20&PlayerID=" \
          + str(player_id) + "&SeasonType=Regular+Season"
    try:
        response = requests.get(url, headers=header, timeout=600)
        data = response.json()['resultSets'][0]['rowSet'][0]
        birthday = str(data[6])
        height = data[10]
        if height is not None and height != "" and height != " ":
            feet, inches = height.split("-")
            height_inches = str(int(feet) * 12 + int(inches))
        else:
            height_inches = ""
        weight = data[11]
        if weight == "0" or weight == 0 or weight == " ":
            weight = ""
        position = data[14]
        draft_year = data[26]
        draft_pos = data[28]

        csv.write(str(player_id) + "," + birthday + "," + height_inches + "," + str(weight) +
                  "," + position + "," + str(draft_year) + "," + str(draft_pos) + "\n")
    except json.JSONDecodeError:
        print("issue connecting to API")
    except KeyError:
        print("couldn't find the API endpoint for player with ID=" + str(player_id))
        pass
csv.close()




