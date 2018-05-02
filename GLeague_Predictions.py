from flask import Flask, render_template, request, jsonify
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
        last = None
        i = 0
        while i < 4:
            random = randint(1, len(players) - 1)
            if random != last:
                random_nums.append(random)
                last = random
                i += 1

        for num in random_nums:
            row = players[num]
            player_id = row[1]
            print(player_id)
            player = Player(player_id)
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
        last = None
        i = 0
        while i < 4:
            random = randint(1, len(players) - 1)
            if random != last:
                random_nums.append(random)
                last = random
                i += 1
        for num in random_nums:
            row = players[num]
            player_id = row[1]
            print(player_id)
            player = Player(player_id)
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

    return render_template('content.html', player=player_obj, players_json=players_json)


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
    neighbors = player.getNBANeighbors(data_given=nba_indexes)
    for x in neighbors:
        attrs = x.__dict__
        neighbors_json.append(attrs)
    return jsonify(result=neighbors_json)


if __name__ == '__main__':
    app.run()

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


nba_stats = {    'fgper': 'FGper',
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