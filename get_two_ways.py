import requests
import os
import json
import global_items

def scrape():
    wd = os.getcwd()

    if wd == "/home/cfisher5":
        two_ways = "GLeague-Predictions/data/two_ways.csv"
    else:
        two_ways = "data/two_ways.csv"

    two_ways_csv = open(two_ways, 'w')
    url = "http://stats.gleague.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=1&LeagueID=20&Season=" + global_items.season
    two_ways_csv.write('ID,Two_Way_Flag,NBA_Team\n')

    try:
        response = requests.get(url, headers=global_items.header, timeout=100)
        data = response.json()['resultSets'][0]['rowSet']
    except json.JSONDecodeError:
        print("unable to reach API")
        two_ways_csv.close()
        os.remove(two_ways)
        return False

    print("grabbing g league two way contract info")
    for player in data:
        player_id = str(player[0])
        two_way_flag = str(player[12])
        if two_way_flag == "1":
            team = str(player[13])
            two_ways_csv.write(player_id + "," + two_way_flag + "," + team + "\n")

    two_ways_csv.close()
    return True


worked = scrape()


