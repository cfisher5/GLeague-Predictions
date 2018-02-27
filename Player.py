from analytics import *
from Neighbor import *
from fake_useragent import UserAgent
import requests
import json


class Player:

    def __init__(self, id, name):
        self.name = name
        self.team = None
        self.id = id
        self.height = None
        self.weight = None
        self.position = None
        self.bg = None
        self.age = None
        self.gp = None
        self.threepm = None
        self.ast = None
        self.fga = None
        self.pts = None
        self.reb = None
        self.gnb_cluster = None
        self.knn_cluster = None
        self.neighbors = []
        self.gleague_id = self.get_data()
        self.pic_id = id
        self.get_misc_data()
        self.gamelog = self.get_game_log()

    def get_analytics(self):
        test_data = [[self.threepm, self.ast, self.fga, self.pts, self.reb]]
        X_train, y, test = format_data(test_data)
        pred = gaussian_nb(X_train, y, test)
        self.gnb_cluster = pred
        self.knn_cluster, comps = knn(X_train, y, test)
        for neighbor in comps:
            with open("data/training_data.csv", "r") as player_file:
                players = csv.reader(player_file, delimiter=',')
                next(players, None)
                for p in players:
                    if str(neighbor) == str(p[0]):
                        neigh = Neighbor(p[2],p[1])
                        self.neighbors.append(neigh)

    def get_data(self):

        with open('data/gleague_data.csv', 'r') as gleague_file:
            players = csv.reader(gleague_file, delimiter=',')
            next(players, None)
            for p in players:
                if self.id == p[1]:
                    gleague_id = p[1]
                    self.team = p[2]
                    self.name = p[0]
                    self.age = p[3]
                    self.gp = p[4]
                    self.fga = p[5]
                    self.threepm = p[6]
                    self.reb = p[7]
                    self.ast = p[8]
                    self.pts = p[9]

                    return gleague_id
        print("Unable to find " + self.name)

    def get_misc_data(self):
        url = "http://stats.gleague.nba.com/stats/commonplayerinfo?LeagueID=20&PlayerID=" + str(self.id) + "&SeasonType=Regular+Season"
        data = None
        try:
            ua = UserAgent()
            header = {'User-Agent': str(ua.random)}
            response = requests.get(url, headers=header)
            data = response.json()['resultSets'][0]['rowSet']
        except json.JSONDecodeError:
            print("unable to reach API")

        for obj in data:
            self.bg = obj[9]
            self.height = obj[10]
            self.weight = obj[11]
            self.position = obj[14]

    def split_id(self):
        pic_id = self.gleague_id.split("/")[3]
        return pic_id

    def get_game_log(self):
        log = []
        try:
            ua = UserAgent()
            header = {"User-Agent": str(ua.random)}
            response = requests.get("http://stats.gleague.nba.com/stats/playergamelog?LeagueID=20&PlayerID=" + str(
                self.id) + "&Season=2017-18&SeasonType=Regular+Season", headers=header)
            data = response.json()['resultSets'][0]['rowSet']
            try:
                for i in range(0, 10):
                    log.append(data[i])
            except IndexError:
                pass

        except json.JSONDecodeError:
            print("couldnt access api")
            log = None
        return log
