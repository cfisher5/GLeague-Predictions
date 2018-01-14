from urllib.request import urlopen
from bs4 import BeautifulSoup
from analytics import *
import csv
from Neighbor import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time


class Player:

    def __init__(self, id, name):
        self.name = name
        self.team = None
        self.id = id
        self.height = "N/A"
        self.weight = "N/A"
        self.position = "N/A"
        self.age = "N/A"
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


    def get_height_weight(self):
        url = "http://stats.gleague.nba.com" + self.gleague_id
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        driver_player = webdriver.Chrome(chrome_options=options)

        driver_player.set_page_load_timeout(8)
        try:
            driver_player.get(url)
            time.sleep(5)
        except TimeoutException:
            driver_player.execute_script("window.stop();")
            print("window stopped")

        source_player = driver_player.page_source
        soup_player = BeautifulSoup(source_player, "html.parser")
        driver_player.quit()
        div = soup_player.find("div", {'class': 'player-summary__bio'}).find('div').string

        try:
            weight, height = div.strip().split(" / ")
        except ValueError:
            weight = "N/A"
            height = "N/A"

        self.weight = weight
        self.height = height

    def split_id(self):
        pic_id = self.gleague_id.split("/")[3]
        return pic_id
