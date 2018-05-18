from fake_useragent import UserAgent
import requests
import json
from NBAComparison import *
import global_items
import pandas as pd
import csv

def scrape_positions():
    csv_file = open("data/positions.csv", "w")
    all_players = json.load(open("data/players_json.txt"))
    for player in all_players:
        player_id = player['value']
        url = "http://stats.gleague.nba.com/stats/commonplayerinfo?LeagueID=20&PlayerID=" + str(
            player_id) + "&SeasonType=Regular+Season"
        data = None
        position = None
        try:
            ua = UserAgent()
            header = {'User-Agent': str(ua.random)}
            response = requests.get(url, headers=header)
            data = response.json()['resultSets'][0]['rowSet']
            for obj in data:
                position = obj[14]
                print(position)
        except json.JSONDecodeError:
            print("unable to reach API")

        if position == "" or position is None:
            print("trying nba csv")
            with open("data/nba_player_data.csv", "r") as nba_data:
                players = csv.reader(nba_data)
                next(players, None)
                for nba_player in players:
                    if player_id == nba_player[0]:
                        position = nba_player[4]
                        print(position)
                        break

        if position == "" or position is None:
            print("trying nba json")
            url_json = "https://data.nba.com/data/10s/v2015/json/mobile_teams/dleague/2017/players/playercard_" + str(
                player_id) + "_02.json"
            try:
                response = requests.get(url_json, headers=global_items.header)
                jsondata = response.json()['pl']
                position = jsondata['pos']
                print(position)
            except json.JSONDecodeError:
                print("unable to reach s.data.nba API")

        if position is None:
            print("unable to find position from any source")
        elif position == "Guard":
            position = "G"
        elif position == "Forward":
            position = "F"
        elif position == "Guard-Forward":
            position = "G-F"
        elif position == "Center":
            position = "C"
        elif position == "Forward-Center":
            position = "F-C"

        csv_file.write(player_id + "," + position + "\n")
    csv_file.close()


# scrape_positions()
data = pd.read_csv(open("data/positions.csv", "r"), sep=",")





