from flask import Flask, render_template, request, jsonify
from Player import *
import csv
import json
import random

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
    with open('data/gleague_data.csv', 'r') as all_players:
        players = list(csv.reader(all_players, delimiter=','))
        players.pop(0)
        random_players = random.sample(players, 4)

        for p in random_players:
            player_name = p[0]
            player_id = p[1]
            player_team = p[2]
            player_age = p[3]
            player = (player_id, player_name, player_team, player_age)
            prospects.append(player)

    return render_template('index.html', players_json=players_json, prospects=prospects)


@app.errorhandler(500)
def page_not_found(e):

    with open('data/players_json.txt', 'r') as infile:
        players_json = infile.read()

    prospects = []
    with open('data/gleague_data.csv', 'r') as all_players:
        players = list(csv.reader(all_players, delimiter=','))
        players.pop(0)
        random_players = random.sample(players, 4)

        for p in random_players:
            player_name = p[0]
            player_id = p[1]
            player_team = p[2]
            player_age = p[3]
            player = (player_id, player_name, player_team, player_age)
            prospects.append(player)

    error_msg = "Please make sure you select a valid player!"
    return render_template('index.html', players_json=players_json, error_msg=error_msg, prospects=prospects), 500


@app.route('/get')
def show_info():

    with open('data/players_json.txt', 'r') as infile:
        players_json = infile.read()

    player_id = request.args.get('player_id')
    print("player id: " + player_id)

    if "/" in player_id:
        player_id = player_id.split("/")[3]
    player_obj = Player(player_id)

    neighbors = player_obj.get_nba_neighbors()
    neighbors_json = list()
    if neighbors is not None:
        for x in neighbors:
            attrs = x.__dict__
            neighbors_json.append(attrs)
    else:
        neighbors_json = None

    return render_template('content.html', player=player_obj, players_json=players_json, neighbors_json=neighbors_json)


@app.route('/_getComps')
def getNBAComps():
    data = json.loads(request.args.get('data'))
    data_comps = data["data_selected"]
    gleague_indexes = []
    nba_indexes = []
    playerID = request.args.get('playerID')
    player = Player(playerID)
    height = None
    weight = None
    for item in data_comps:
        if item == "height":
            height = True
            nba_indexes.append(get_nba_index(item))
        elif item == "weight":
            weight = True
            nba_indexes.append(get_nba_index(item))

        else:
            gleague_indexes.append(get_gleague_index(item))
            nba_indexes.append(get_nba_index(item))

    player.get_predictions(data_given=gleague_indexes, height=height, weight=weight)
    neighbors_json = []
    neighbors = player.get_nba_neighbors(data_given=nba_indexes)
    for x in neighbors:
        attrs = x.__dict__
        neighbors_json.append(attrs)

    return jsonify(result=neighbors_json)


gleague_preds = {'fgper': 7,
                 'threeper': 8,
                 'ftper': 9,
                 'pts': 1,
                 'reb': 2,
                 'ast': 3,
                 'stl': 4,
                 'blk': 5}


def get_gleague_index(data):
    return gleague_preds[data]


nba_stats = {'fgper': 'FGper',
             'threeper': 'threeper',
             'ftper': 'FTper',
             'pts': 'PTS',
             'reb': 'REB',
             'ast': 'AST',
             'stl': 'STL',
             'blk': 'BLK',
             'height': 'height_inches',
             'weight': 'weight'}


def get_nba_index(data):
    return nba_stats[data]


if __name__ == '__main__':
    app.run()
