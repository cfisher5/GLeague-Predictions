from analytics import *
from Neighbor import *
from fake_useragent import UserAgent
import requests
import json
from NBAComparison import *
from datetime import datetime
import global_items
import pandas as pd
from scipy import stats


class Player:

    def __init__(self, id):
        self.name = None
        self.team = None
        self.id = id
        self.height = None
        self.weight = None
        self.position = None
        self.nba_team = None
        self.two_way = self.check_two_way()
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
        self.nba_comps = self.get_nba_neighbors()
        self.get_analytics()
        self.cluster_color = self.get_color()
        self.fix_position()
        self.stats = self.gather_stats()
        self.advanced_stats = self.get_advanced_stats()
        self.shooting_stats = self.get_shooting_stats()
        self.percentile_array = [self.get_percentiles('box'), self.get_percentiles('advanced'), self.get_percentiles('shooting')]
        self.mpg = str(round(float(self.min) / float(self.gp),1))

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

    def get_nba_neighbors(self, data_given=None):
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
        print("Unable to find " + str(self.name))

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
            if self.bg is not None and len(self.bg.split("/")) == 2:
                bg1, bg2 = self.bg.split("/")
                if bg1.strip() == bg2.strip():
                    self.bg = bg1
                else:
                    self.bg = bg1.strip() + "/" + bg2.strip()
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
        game_dates = []
        try:
            ua = UserAgent()
            header = {"User-Agent": str(ua.random)}
            response = requests.get("http://stats.gleague.nba.com/stats/playergamelog?LeagueID=20&PlayerID=" + str(
                self.id) + "&Season=2017-18&SeasonType=Regular+Season", headers=header)
            data = response.json()['resultSets'][0]['rowSet']
            try:
                for i in range(0, len(data)):
                    datetime_object = datetime.strptime(data[i][3], '%b %d, %Y').date()
                    shotchart_date = datetime_object.strftime("%m-%d-%Y")
                    game_dates.append(shotchart_date)
                    data[i][3] = datetime_object
                    log.append(data[i])
            except IndexError:
                pass

        except json.JSONDecodeError:
            print("couldnt access api")
            log = None
            return log

        game_dates = game_dates[::-1]
        return [log, game_dates]


    def get_color(self):
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

    def check_two_way(self):
        with open("data/two_ways.csv", "r") as two_ways:
            players = csv.reader(two_ways)
            next(players, None)
            for player in players:
                if self.id == player[0]:
                    if player[1] == "1":
                        nba_team = player[2]
                        with open("data/nba_teams.csv", "r") as nba_teams:
                            teams = csv.reader(nba_teams)
                            next(teams, None)
                            for team in teams:
                                if nba_team == team[0]:
                                    self.nba_team = team[1]
                                    break
                        return True
                    else:
                        self.nba_team = None
                        return False

    def fix_position(self):
        if self.position == "Guard":
            self.position = "G"
        if self.position == "Forward":
            self.position = "F"
        if self.position == "Guard-Forward":
            self.position = "G-F"
        if self.position == "Center":
            self.position = "C"
        if self.position == "Forward-Center":
            self.position = "F-C"

    def get_advanced_stats(self):
        stats = {}
        stats_array = []
        with open("data/gleague_advanced.csv", "r") as adv_stats:
            players = csv.reader(adv_stats)
            next(players, None)
            for player in players:
                if self.id == player[0]:
                    stats['ORTG'] = player[2]
                    stats_array.append(player[2])
                    stats['DRTG'] = player[3]
                    stats_array.append(player[3])
                    stats['NRTG'] = player[4]
                    stats_array.append(player[4])
                    stats['ASTPER'] = player[5]
                    stats_array.append(float(player[5]) * 100.0)
                    stats['OREBPER'] = player[6]
                    stats_array.append(float(player[6]) * 100.0)
                    stats['DREBPER'] = player[7]
                    stats_array.append(float(player[7]) * 100.0)
                    stats['eFG'] = player[8]
                    stats_array.append(float(player[8]) * 100.0)
                    stats['TS'] = player[9]
                    stats_array.append(float(player[9]) * 100.0)
                    stats['USG'] = player[10]
                    stats_array.append(float(player[10]) * 100.0)
                    break

        stat_labels = ["ORtg","DRtg","Net Rating","AST%","OREB%","DREB%","eFG%","TS%","USG%"]
        return [stat_labels, stats, stats_array]

    def get_shooting_stats(self):

        locations = ['Right Corner 3', 'Restricted Area (RA)', 'Paint (Non RA)', 'Mid-Range', 'Left Corner 3', 'Above the Break 3']
        accuracy = []
        frequency = []
        raw_shots = []
        df = pd.read_csv("data/shooting.csv")
        min_df = pd.read_csv("data/min.csv")
        merged_df = pd.merge(left=df, right=min_df, how='inner', on="PLAYER_ID")

        query_str = "PLAYER_ID == " + str(self.id)
        player_row = merged_df.query(query_str)

        i = player_row.index[0]

        if len(player_row) == 1:

            total_shot_attempts = 0.0
            total_shot_attempts += player_row['RA_FGA'].get(i)
            total_shot_attempts += player_row['Paint_FGA'].get(i)
            total_shot_attempts += player_row['Mid-Range_FGA'].get(i)
            total_shot_attempts += player_row['Left_Corner_FGA'].get(i)
            total_shot_attempts += player_row['Right_Corner_FGA'].get(i)
            total_shot_attempts += player_row['Above_Break_FGA'].get(i)

            types = ["Right_Corner", "RA", "Paint", "Mid-Range", "Left_Corner", "Above_Break"]
            index = 0
            for shot_type in types:
                fgper = player_row[shot_type + '_FG_PCT'].get(i)
                accuracy.append(float(fgper))
                fga = player_row[shot_type + '_FGA'].get(i)
                shot_freq = fga / total_shot_attempts
                frequency.append(shot_freq)
                fgm = player_row[shot_type + '_FGM'].get(i)
                raw_shots.append(str(fgm).replace(".0", "") + "/" + str(fga).replace(".0", ""))
                index += 1
            return [locations, frequency, accuracy, raw_shots]

        else:
            return None

    def get_percentiles(self, stat_type):

        if stat_type == "box":
            # Box score percentiles
            data = pd.read_csv(open("data/gleague_data.csv", "r"), sep=",")
            positions = pd.read_csv(open("data/positions.csv", "r"), sep=",")
            data = data.query("MIN > 200.0")
            merged_df = pd.merge(left=data, right=positions, how='inner', on='ID')

            # get query
            if 'G' in self.position:
                query_string = "POS == 'G' or POS == 'G-F' or POS == 'F-G'"
            elif 'F' in self.position:
                query_string = "POS == 'F' or POS == 'G-F' or POS == 'F-G' or POS=='F-C' or POS=='C-F'"
            else:
                query_string = "POS == 'C' or POS == 'F-C' or POS == 'C-F'"

            subset_pos = merged_df.query(query_string)
            arr = list()
            arr.append(stats.percentileofscore(subset_pos['FGA'], float(self.fga)))
            arr.append(stats.percentileofscore(subset_pos['FGP'], float(self.fgper)/100.0))
            arr.append(stats.percentileofscore(subset_pos['3PA'], float(self.threepa)))
            arr.append(stats.percentileofscore(subset_pos['3PPER'], float(self.threeper)/100.0))
            arr.append(stats.percentileofscore(subset_pos['PTS'], float(self.pts)))
            arr.append(stats.percentileofscore(subset_pos['REB'], float(self.reb)))
            arr.append(stats.percentileofscore(subset_pos['AST'], float(self.ast)))
            arr.append(stats.percentileofscore(subset_pos['FTPER'], float(self.ftper)/100.0))
            arr.append(stats.percentileofscore(subset_pos['STL'], float(self.stl)))
            arr.append(stats.percentileofscore(subset_pos['BLK'], float(self.blk)))
            arr.append(100.0 - stats.percentileofscore(subset_pos['TOV'], float(self.tov)))

            percentile_colors = self.get_percentiles_colors(arr)

            normalized_arr = list()
            for element in arr:
                norm = element - 50.0
                if norm > 50.0:
                    norm = 50.0
                elif norm < -50.0:
                    norm = -50.0

                normalized_arr.append(norm)

            return [arr, normalized_arr, percentile_colors]

        # advanced percentiles
        elif stat_type == "advanced":

            adv_stats = self.advanced_stats[1]
            data = pd.read_csv(open("data/gleague_advanced.csv", "r"), sep=",")
            positions = pd.read_csv(open("data/positions.csv", "r"), sep=",")
            min = pd.read_csv(open("data/min.csv", "r"), sep=",")
            merged_df = pd.merge(left=pd.merge(left=data, right=positions, how='inner', on='ID'), right=min, left_on='ID', right_on='PLAYER_ID', how='inner')
            merged_df = merged_df.query("MIN > 200.0")
            # get query
            if 'G' in self.position:
                query_string = "POS == 'G' or POS == 'G-F' or POS == 'F-G'"
            elif 'F' in self.position:
                query_string = "POS == 'F' or POS == 'G-F' or POS == 'F-G' or POS=='F-C' or POS=='C-F'"
            else:
                query_string = "POS == 'C' or POS == 'F-C' or POS == 'C-F'"

            subset_pos = merged_df.query(query_string)
            arr = list()
            arr.append(stats.percentileofscore(subset_pos['ORTG'], float(adv_stats['ORTG'])))
            arr.append(100.0 - stats.percentileofscore(subset_pos['DRTG'], float(adv_stats['DRTG'])))
            arr.append(stats.percentileofscore(subset_pos['NRTG'], float(adv_stats['NRTG'])))
            arr.append(stats.percentileofscore(subset_pos['ASTPER'], float(adv_stats['ASTPER'])))
            arr.append(stats.percentileofscore(subset_pos['OREBPER'], float(adv_stats['OREBPER'])))
            arr.append(stats.percentileofscore(subset_pos['DREBPER'], float(adv_stats['DREBPER'])))
            arr.append(stats.percentileofscore(subset_pos['eFG'], float(adv_stats['eFG'])))
            arr.append(stats.percentileofscore(subset_pos['TS'], float(adv_stats['TS'])))
            arr.append(stats.percentileofscore(subset_pos['USG'], float(adv_stats['USG'])))

            percentile_colors = self.get_percentiles_colors(arr)

            normalized_arr = list()
            for element in arr:
                norm = element - 50.0
                if norm > 50.0:
                    norm = 50.0
                elif norm < -50.0:
                    norm = -50.0

                normalized_arr.append(norm)

            return [arr, normalized_arr, percentile_colors]

        elif stat_type == "shooting":

            shooting_stats = self.shooting_stats[2]
            data = pd.read_csv(open("data/shooting.csv", "r"), sep=",")
            positions = pd.read_csv(open("data/positions.csv", "r"), sep=",")
            min = pd.read_csv(open("data/min.csv", "r"), sep=",")
            merged_df = pd.merge(left=pd.merge(left=data, right=positions, how='inner', left_on='PLAYER_ID', right_on='ID'), right=min, on='PLAYER_ID', how='inner')
            merged_df = merged_df.query("MIN > 200.0")
            # get query
            if 'G' in self.position:
                query_string = "POS == 'G' or POS == 'G-F' or POS == 'F-G'"
            elif 'F' in self.position:
                query_string = "POS == 'F' or POS == 'G-F' or POS == 'F-G' or POS=='F-C' or POS=='C-F'"
            else:
                query_string = "POS == 'C' or POS == 'F-C' or POS == 'C-F'"

            subset_pos = merged_df.query(query_string)
            arr = list()
            arr.append(stats.percentileofscore(subset_pos['Right_Corner_FG_PCT'], float(shooting_stats[0])))
            arr.append(stats.percentileofscore(subset_pos['RA_FG_PCT'], float(shooting_stats[1])))
            arr.append(stats.percentileofscore(subset_pos['Paint_FG_PCT'], float(shooting_stats[2])))
            arr.append(stats.percentileofscore(subset_pos['Mid-Range_FG_PCT'], float(shooting_stats[3])))
            arr.append(stats.percentileofscore(subset_pos['Left_Corner_FG_PCT'], float(shooting_stats[4])))
            arr.append(stats.percentileofscore(subset_pos['Above_Break_FG_PCT'], float(shooting_stats[5])))

            percentile_colors = self.get_percentiles_colors(arr)

            normalized_arr = list()
            for element in arr:
                norm = element - 50.0
                if norm > 50.0:
                    norm = 50.0
                elif norm < -50.0:
                    norm = -50.0

                normalized_arr.append(norm)

            return [arr, normalized_arr, percentile_colors]

    def gather_stats(self):

        stats_headers = ["FGA","FG%","3PA","3P%","PTS","REB","AST","FT%","STL","BLK","TOV"]

        stats = [str(self.fga), str(self.fgper)+"%", str(self.threepa), str(self.threeper)+"%", str(self.pts), str(self.reb), str(self.ast),
                 str(self.ftper)+"%", str(self.stl), str(self.blk), str(self.tov)]

        return [stats_headers, stats]

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
                color_arr.append("#FF8080")

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

        return color_arr
