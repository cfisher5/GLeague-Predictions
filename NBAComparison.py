import csv


class NBAComparison:

    def __init__(self, id):
        self.name = None
        self.id = id
        self.team_id = None
        self.team = None
        self.nba_g = None
        self.nba_min = None
        self.nba_threeper = None
        self.nba_ftper = None
        self.nba_ast = None
        self.nba_fgper = None
        self.nba_pts = None
        self.nba_reb = None
        self.nba_stl = None
        self.nba_blk = None
        self.nba_tov = None
        self.height = None
        self.weight = None
        self.position = None

    def populate(self):
        with open("data/nba36.csv", "r") as nba:
            nba_file = csv.reader(nba, delimiter=",")
            next(nba_file, None)
            for row in nba_file:
                if self.id == row[1]:
                    self.name = row[2]
                    self.team_id = row[3]
                    self.team = row[4]
                    self.nba_g = row[5]
                    self.nba_min = int(float(row[6]))
                    self.nba_pts = round(float(row[7]), 1)
                    self.nba_reb = round(float(row[8]), 1)
                    self.nba_ast = round(float(row[9]), 1)
                    self.nba_stl = round(float(row[10]), 1)
                    self.nba_blk = round(float(row[11]), 1)
                    self.nba_tov = round(float(row[12]), 1)
                    self.nba_fgper = round(float(row[13]) * 100, 1)
                    self.nba_threeper = round(float(row[14]) * 100, 1)
                    self.nba_ftper = round(float(row[15]) * 100, 1)
                    break

        with open("data/nba_player_data.csv", "r") as nba_data:
            players = csv.reader(nba_data)
            next(players, None)
            for player in players:
                if self.id == player[0]:
                    self.height = player[1]
                    self.weight = player[3]
                    self.position = player[4]
                    break




