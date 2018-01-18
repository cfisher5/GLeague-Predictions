from flask import Flask, render_template, request
from Player import *
import csv
import requests
import json
from random import randint
app = Flask(__name__)


@app.route('/')
def begin():
    with open('data/players_json.txt', 'r') as infile:
        players_json = infile.read()

    # with open('data/prospects_to_watch.csv', 'r') as prospects_file:
    #     players = csv.reader(prospects_file, delimiter=',')
    #     next(players, None)
    #     index = 0
    #     for p in players:
    #         if index >= 3:
    #             break
    #         index += 1
    #         player_name = p[0]
    #         player_id = p[1].replace('http://stats.gleague.nba.com', '')
    #         player = Player(player_id, player_name)
    #         prospects.append(player)
    prospects = []
    random_nums = []
    with open('data/gleague_data.csv', 'r') as all_players:
        players = list(csv.reader(all_players, delimiter=','))
        print(len(players))
        for i in range(0, 3):
            random_nums.append(randint(1, len(players) - 1))
        for num in random_nums:
            row = players[num]
            player_name = row[0]
            player_id = row[1]
            player = Player(player_id, player_name)
            prospects.append(player)

    return render_template('index.html', players_json=players_json, prospects=prospects)


@app.errorhandler(500)
def page_not_found(e):

    with open('data/players_json.txt', 'r') as infile:
        players_json = infile.read()
    random_nums = []
    prospects = []
    with open('data/gleague_data.csv', 'r') as all_players:
        players = list(csv.reader(all_players, delimiter=','))
        for i in range(0, 3):
            random_nums.append(randint(1, len(players) - 1))
        for num in random_nums:
            row = players[num]
            player_name = row[0]
            player_id = row[1]
            player = Player(player_id, player_name)
            prospects.append(player)

    error_msg = "Please make sure you select a valid player!"
    return render_template('index.html', players_json=players_json, error_msg=error_msg, prospects=prospects), 500


@app.route('/get', methods=['get'])
def show_info():
    player_id = request.args.get('player_id')
    if "/" in player_id:
        player_id = player_id.split("/")[3]
    player_name = request.args.get('player_list')
    player_obj = Player(player_id, player_name)
    print(player_id)
    # game_log = get_five_game_log(player_id)
    # player_obj.get_height_weight()
    player_obj.get_analytics()
    with open('data/players_json.txt', 'r') as infile:
        players_json = infile.read()
    return render_template('content.html', player=player_obj, players_json=players_json)



def get_five_game_log(player_id):
    five_games = []
    try:
        response = requests.get("http://stats.gleague.nba.com/stats/playergamelog?LeagueID=20&PlayerID=" + str(player_id) + "&Season=2017-18&SeasonType=Regular+Season")
        data = response.json()['resultSets'][0]['rowSet']
        for i in range(0, 5):
            five_games.append(data[i])

    except json.JSONDecodeError:
        print("couldnt access api")
        five_games = None
    return five_games

if __name__ == '__main__':
    app.run()