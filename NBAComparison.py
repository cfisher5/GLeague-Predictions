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
                    self.nba_min = row[6]
                    self.nba_pts = row[7]
                    self.nba_reb = row[8]
                    self.nba_ast = row[9]
                    self.nba_stl = row[10]
                    self.nba_blk = row[11]
                    self.nba_tov = row[12]
                    self.nba_fgper = row[13]
                    self.nba_threeper = row[14]
                    self.nba_ftper = row[15]
                    break






