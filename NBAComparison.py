import csv
import pandas as pd
from scipy import stats


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
        self.populate()
        self.percentile_color_array = None
        self.stats = self.gather_stats()
        self.percentile_array = self.get_percentiles()
        self.mpg = str(round(float(self.nba_min) / float(self.nba_g), 1))

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

    def get_percentiles(self):

        per_36_data = pd.read_csv(open("data/nba36.csv", "r"), sep=",")
        positions = pd.read_csv(open("data/nba_player_data.csv", "r"), sep=",")
        per_36_data = per_36_data.query("TotalMin > 300.0")
        merged_df = pd.merge(left=per_36_data, right=positions, how='inner', on='ID')

        # get query
        if 'G' in self.position:
            query_string = "pos == 'G' or pos == 'G-F' or pos == 'F-G'"
        elif 'F' in self.position:
            query_string = "pos == 'F' or pos == 'G-F' or pos == 'F-G' or pos =='F-C' or pos =='C-F'"
        else:
            query_string = "pos == 'C' or pos == 'F-C' or pos == 'C-F'"
        subset_pos = merged_df.query(query_string)
        arr = list()

        arr.append(stats.percentileofscore(subset_pos['PTS'], float(self.nba_pts)))
        arr.append(stats.percentileofscore(subset_pos['REB'], float(self.nba_reb)))
        arr.append(stats.percentileofscore(subset_pos['AST'], float(self.nba_ast)))
        arr.append(stats.percentileofscore(subset_pos['FGper'], float(self.nba_fgper)/100.0))
        arr.append(stats.percentileofscore(subset_pos['threeper'], float(self.nba_threeper)/100.0))
        arr.append(stats.percentileofscore(subset_pos['FTper'], float(self.nba_ftper)/100.0))
        arr.append(stats.percentileofscore(subset_pos['STL'], float(self.nba_stl)))
        arr.append(stats.percentileofscore(subset_pos['BLK'], float(self.nba_blk)))
        arr.append(100.0 - stats.percentileofscore(subset_pos['TOV'], float(self.nba_tov)))

        self.get_percentiles_colors(arr)

        normalized_arr = list()
        for element in arr:
            norm = element - 50.0
            if norm > 50.0:
                norm = 50.0
            elif norm < -50.0:
                norm = -50.0

            normalized_arr.append(norm)

        return arr, normalized_arr

    def gather_stats(self):

        stats_headers = ["PTS","REB","AST","FG%","3P%","FT%","STL","BLK","TOV"]

        stats = [str(self.nba_pts), str(self.nba_reb), str(self.nba_ast),str(self.nba_fgper)+"%", str(self.nba_threeper)+"%",
                 str(self.nba_ftper)+"%", str(self.nba_stl), str(self.nba_blk), str(self.nba_tov)]

        return stats_headers, stats

    def get_percentiles_colors(self, array):
        color_arr = list()
        for data in array:
            if data < 10.0:
                color_arr.append("#8B0000")

            elif data < 20.0:
                color_arr.append("#B22222")

            elif data < 30.0:
                color_arr.append("#CD5C5C")

            elif data < 40.0:
                color_arr.append("#F08080")

            elif data < 60.0:
                color_arr.append("#94948f")

            elif data < 70.0:
                color_arr.append("#3CB371")

            elif data < 80.0:
                color_arr.append("#228B22")

            elif data < 90.0:
                color_arr.append("#008000")

            else:
                color_arr.append("#006400")

        self.percentile_color_array = color_arr



