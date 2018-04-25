from analytics import *
from Neighbor import *
from fake_useragent import UserAgent
import requests
import json
from NBAComparison import *
from datetime import datetime
import global_items
class Player:

    def __init__(self, id):
        self.name = None
        self.team = None
        self.id = id
        self.height = None
        self.weight = None
        self.position = None
        self.bg = None
        self.age = None
        self.gp = None
        self.min = None
        self.threepm = None
        self.threepa = None
        self.threeper = None
        self.ftm = None
        self.fta = None
        self.ftper = None
        self.ast = None
        self.stl = None
        self.blk = None
        self.tov = None
        self.fgm = None
        self.fga = None
        self.fgper = None
        self.pts = None
        self.reb = None
        self.gnb_cluster = None
        self.knn_cluster = None
        self.neighbors = []
        self.gleague_id = self.get_data()
        self.pic_id = id
        self.get_misc_data()
        self.height_inches = self.convert_height()
        self.gamelog = self.get_game_log()
        self.predicted_nba_stats = self.get_predictions()
        self.nba_comps = self.getNBANeighbors()
        self.get_analytics()
        self.cluster_color = self.getColor()

    def get_analytics(self):
        if self.height != "":
            test_data = [[self.threepm, self.ast, self.fga, self.pts, self.reb, self.height_inches, self.weight]]
            X_train, y, test = format_data(test_data, True)
        else:
            test_data = [[self.threepm, self.ast, self.fga, self.pts, self.reb]]
            X_train, y, test = format_data(test_data, False)

        self.gnb_cluster = gaussian_nb(X_train, y, test)
        self.knn_cluster, comps = knn(X_train, y, test)
        for neighbor in comps:
            with open("data/training_data.csv", "r") as player_file:
                players = csv.reader(player_file, delimiter=',')
                next(players, None)
                for p in players:
                    if str(neighbor) == str(p[0]):
                        neigh = Neighbor(p[2],p[1])
                        self.neighbors.append(neigh)


    def get_predictions(self, data_given=None, height=None, weight=None):
        with open('data/gleague_projections.csv', 'r') as predictions:
            preds = csv.reader(predictions, delimiter=",")
            next(preds, None)
            for row in preds:
                if self.id == row[0]:
                    if data_given is not None:
                        print("grabbing custom data")
                        data = []
                        for item in data_given:
                            data.append(row[item])
                        if height is not None:
                            data.append(int(self.height_inches))
                        if weight is not None:
                            data.append(int(self.weight))
                        self.predicted_nba_stats = [data]
                        return [data]
                    else:
                        if self.height == "":
                            data = [row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[9]]
                        else:
                            data = [row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[9], int(self.height_inches), int(self.weight)]

                        return [data]
        return None

    def getNBANeighbors(self, data_given=None):
        if self.predicted_nba_stats is None:
            return None

        comps = get_nba_comps(self, self.predicted_nba_stats, data_given=data_given)
        players = []
        num_appended = 0
        for num in comps:
            with open("data/nba_merge.csv", "r") as nba:
                nba_file = csv.reader(nba, delimiter=",")
                next(nba_file, None)
                for row in nba_file:
                    if str(num) == row[0]:
                        if row[1] != self.id and num_appended < 3:
                            num_appended += 1
                            nba_comp = NBAComparison(row[1])
                            nba_comp.populate()
                            players.append(nba_comp)
                            break
        return players

    def get_data(self):

        with open('data/gleague_data.csv', 'r') as gleague_file:
            players = csv.reader(gleague_file, delimiter=',')
            next(players, None)
            for p in players:
                if self.id == p[1]:
                    self.name = p[0]
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
                    self.min = p[10]
                    self.fgm = p[11]
                    self.fgper = round(float(p[12]) * 100, 1)
                    self.threepa = p[13]
                    self.threeper = round(float(p[14]) * 100, 1)
                    self.ftm = p[15]
                    self.fta = p[16]
                    self.ftper = round(float(p[17]) * 100, 1)
                    self.tov = p[18]
                    self.stl = p[19]
                    self.blk = p[20]
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

        if self.height == "":
            with open("data/nba_player_data.csv", "r") as nba_data:
                players = csv.reader(nba_data)
                next(players, None)
                for player in players:
                    if self.id == player[0]:
                        self.height = player[1]
                        self.weight = player[3]
                        self.position = player[4]
                        return

        if self.height == "":
            url_json = "https://data.nba.com/data/10s/v2015/json/mobile_teams/dleague/2017/players/playercard_" + str(self.id) + "_02.json"
            try:
                response = requests.get(url_json, headers=global_items.header)
                jsondata = response.json()['pl']
            except json.JSONDecodeError:
                print("unable to reach s.data.nba API")
                return

            height = jsondata['ht']
            self.height = height
            weight = jsondata['wt']
            self.weight = weight
            self.position = jsondata['pos']

    def convert_height(self):
        height = self.height
        if height == "":
            return None
        feet, inches = height.split("-")
        height_inches = int(feet) * 12 + int(inches)
        return height_inches

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
                for i in range(0, len(data)):
                    datetime_object = datetime.strptime(data[i][3], '%b %d, %Y').date()
                    data[i][3] = datetime_object
                    log.append(data[i])
            except IndexError:
                pass

        except json.JSONDecodeError:
            print("couldnt access api")
            log = None
        return log

    def getColor(self):
        if self.gnb_cluster == "Facilitator":
            color = "#7a69bf"
        elif self.gnb_cluster == "Inside Scoring Big":
            color = "#69bf8b"
        elif self.gnb_cluster == "High Usage Scoring Big":
            color = "#698bbf"
        elif self.gnb_cluster == "Swiss Army Knife":
            color = "#ae69bf"
        elif self.gnb_cluster == "Sweet-Shooting Bucket Getter":
            color = "#bf699c"
        else:
            color = "#69bfbf"
        return color