import csv


class NBAComparison:

    def __init__(self, id, name):
        self.name = name
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


    def populate(self):
        with open("data/nba36.csv", 'r') as nba:
            nba_file = csv.reader(nba, delimiter=",")
            next(nba_file, None)
            for row in nba_file:
                if self.id == row[1]:
                    self.team_id = row[3]
                    self.team = row[4]
                    self.nba_g = row[5]
                    self.nba_min = round(float(row[6]), 0)
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






