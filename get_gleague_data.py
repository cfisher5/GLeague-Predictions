from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

player_json = []
gleague_ids = open('data/gleague_data.csv', 'w')
gleague_ids.write('Name,ID,Team,Age,GP,FGA,3PM,REB,AST,PTS\n')

url = "http://stats.gleague.nba.com/league/player/#!/?Season=2017-18&SeasonType=Regular%20Season&PerMode=Per36"
options = webdriver.ChromeOptions()
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-logging")
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)
driver.set_page_load_timeout(10)
try:
    driver.get(url)
    time.sleep(4)
except TimeoutException:
    driver.execute_script("window.stop();")
    print("window stopped")

for index in range(0, 8):

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('div', {'class': 'table-responsive'}).table.tbody
    for t in table.findAll('tr'):
        player = {}
        all_cols = t.findAll('td')
        player_div = t.find('td', {'class':'first'})
        name = player_div.a.string
        print(name)
        href = player_div.a['href']
        team = all_cols[1].a.string
        age = all_cols[2].string
        gp = all_cols[3].string
        fga = all_cols[8].text
        fga = fga.replace("Shotchart", "").strip()
        threepm = all_cols[10].text
        threepm = threepm.replace("Shotchart", "").strip()
        reb = all_cols[18].string
        ast = all_cols[19].string
        pts = all_cols[26].string

        player['label'] = name
        player['value'] = href

        if player_json.__contains__(player):
            print("ALREADY INSIDE")
            continue

        else:
            player_json.append(player)


        gleague_ids.write(name + "," + href + "," + team + "," + age + "," + gp + "," + fga + "," + threepm + "," + reb + "," + ast + "," + pts + "\n")

    btn = driver.find_element_by_class_name('fa-caret-right')
    btn.click()

driver.quit()

players_file = open('data/players_json.txt', 'w')
players_file.write(str(player_json))
players_file.close()