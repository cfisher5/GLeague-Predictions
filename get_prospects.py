from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

url = "http://stats.gleague.nba.com/league/player/#!/?Season=2017-18&SeasonType=Regular%20Season&PerMode=Per36"
prospects = open('data/prospects_to_watch.csv', 'w')
prospects.write('Player,ID\n')

url = 'http://stats.gleague.nba.com/'
options = webdriver.ChromeOptions()
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-logging")
driver = webdriver.Chrome(chrome_options=options)
driver.set_page_load_timeout(10)

try:
    driver.get(url)
    time.sleep(4)
except TimeoutException:
    driver.execute_script("window.stop();")
    print("window stopped")


source = driver.page_source
soup = BeautifulSoup(source, "html.parser")
driver.quit()

carousel = soup.find("div", {'class': 'stats-prospect-watch'})
ids = carousel.findAll("a", {'class': 'more_stats'})
player_names = carousel.findAll("h2")

for player, href in zip(player_names, ids):
    print(player.string)
    print(href['href'])
    prospects.write(player.string + "," + href['href'] + '\n')


prospects.close()
