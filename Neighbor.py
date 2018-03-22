import csv
import math


class Neighbor:

    def __init__(self, realgm_id, name):
        self.name = name
        self.bref_id = None
        self.gleague_cluster = None
        self.nba_cluster = None
        self.height = None
        self.weight = None
        self.position = "N/A"
        self.gl_threepm = None
        self.gl_g = None
        self.gl_ast = None
        self.gl_fga = None
        self.gl_pts = None
        self.gl_reb = None
        self.nba_g = None
        self.nba_threepm = None
        self.nba_ast = None
        self.nba_fga = None
        self.nba_pts = None
        self.nba_reb = None
        self.pic_id = self.get_data(realgm_id)

    def get_data(self, realgm_id):

        with open('data/training_data.csv', 'r') as training:
            players = csv.reader(training, delimiter=',')
            next(players, None)
            for player in players:
                if player[2] == realgm_id:
                    self.height = str(math.floor(int(player[9]) / 12)) + "-" + str(int(player[9]) % 12)
                    self.weight = player[10]
                    break

        with open('data/2010-17_dataset_clustered.csv', 'r') as database:
            rows = csv.reader(database, delimiter=",")
            next(rows, None)
            next(rows, None)
            for player in rows:
                if realgm_id == player[152]:
                    self.bref_id = player[153]
                    self.gleague_cluster = player[82]
                    self.nba_cluster = player[80]
                    self.gl_g = player[40]
                    self.gl_threepm = player[12]
                    self.gl_ast = player[15]
                    self.gl_fga = player[28]
                    self.gl_pts = player[56]
                    self.gl_reb = player[59]
                    self.nba_g = player[119]
                    self.nba_threepm = player[91]
                    self.nba_ast = player[94]
                    self.nba_fga = player[107]
                    self.nba_pts = player[131]
                    self.nba_reb = player[139]
                    pic_id = self.bref_id.split("/")[3].split(".")[0]
                    return pic_id

        return None
