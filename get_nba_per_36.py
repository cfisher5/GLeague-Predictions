import requests
import os
import csv
import json

def scrape():
    wd = os.getcwd()

    if wd == "/home/cfisher5":
        pace_csv = "GLeague-Predictions/data/pace.csv"
        nba_per_36 = "GLeague-Predictions/data/nba36.csv"
        per36_json = "GLeague-Predictions/data/nbaper36.json"
    else:
        nba_per_36 = "data/nba36.csv"
        per36_json = "data/nbaper36.json"
        pace_csv = "data/pace.csv"

    avg_pace = None
    with open(pace_csv, "r") as pace_file:
        pace = csv.reader(pace_file)
        next(pace, None)
        for team in pace:
            if team[0] == "avg":
                avg_pace = float(team[1])
                break

    nba_36 = open(nba_per_36, "w")
    nba_36.write('index,ID,Name,TeamID,Team,GP,TotalMin,PTS,REB,AST,STL,BLK,TOV,FGper,threeper,FTper\n')

    url = "http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
          "&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&" \
          "MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Per36&Period=0" \
          "&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2017-18&SeasonSegment=" \
          "&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="

    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Dnt': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US',
            'Host': 'stats.nba.com',
            'Referer': 'http://stats.nba.com/players/traditional/?sort=PTS&dir=-1',
            'Connection': 'keep-alive',
            'Cookie': '__qca=P0-1808023843-1509330139519; __gads=ID=d2f2596bbb58f01c:T=1509330139:S=ALNI_MaT7n-b9IBB-xvB8pcKOaJC1BkUAQ; _privy_6A673486582982E68B43A020=%7B%22uuid%22%3A%2228a3d7ad-6f73-4ec9-b8e1-4cf5ef2ae0a7%22%2C%22variations%22%3A%7B%7D%2C%22country_code%22%3A%22US%22%7D; optimizelyEndUserId=oeu1511727268075r0.8663817233978857; optimizelyBuckets=%7B%7D; _mkto_trk=id:167-EIT-370&token:_mch-nba.com-1511727269937-39500; _ga=GA1.2.54571634.1509384958; s_fid=3FF52C8893D8DC3F-0876B27F6DC9308A; s_vi=[CS]v1|2CFB466F05033209-400011842000267A[CE]; optimizelySegments=%7B%222704480408%22%3A%22none%22%2C%222707460365%22%3A%22gc%22%2C%222708140383%22%3A%22false%22%2C%222708290386%22%3A%22search%22%2C%223713124431%22%3A%22gc%22%2C%223728264737%22%3A%22search%22%2C%223734713784%22%3A%22false%22%2C%223735704323%22%3A%22none%22%7D; _privy_a=%7B%22referring_domain%22%3A%22gleague.nba.com%22%2C%22referring_url%22%3A%22http%3A%2F%2Fgleague.nba.com%2Fgames%2F20171118%2FLAKRAP%2F%22%2C%22utm_medium%22%3A%22unknown%22%2C%22utm_source%22%3Anull%2C%22search_term%22%3Anull%2C%22initial_url%22%3A%22http%3A%2F%2Flakeland.gleague.nba.com%2F%22%2C%22sessions_count%22%3A2%2C%22pages_viewed%22%3A3%7D; __unam=b2ed6e-15fcdf3d2f5-4b3ade60-3; AMCV_248F210755B762187F000101%40AdobeOrg=-1891778711%7CMCAID%7C2CFB466F05033209-400011842000267A%7CMCIDTS%7C17580%7CMCMID%7C68373101399095200423489720217121077769%7CMCAAMLH-1519514718%7C7%7CMCAAMB-1519514718%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1518917118s%7CNONE%7CMCSYNCSOP%7C411-17587%7CvVersion%7C2.4.0; aam_uuid=68398756077489532373486601900571739190; __insp_wid=954630821; __insp_slim=1521945122677; __insp_nv=true; __insp_targlpu=aHR0cDovL3d3dy5uYmEuY29tL3JhcHRvcnMvd2F5bmUtZW1icnktZmVsbG93c2hpcC8%3D; __insp_targlpt=VGhlIFdheW5lIEVtYnJ5IEZlbGxvd3NoaXAgfCBUb3JvbnRvIFJhcHRvcnM%3D; __insp_norec_sess=true; ug=5a4f2f0205fde10a3c26e1057b001fb4; AAMC_nba_0=REGION%7C9%7CAMSYNCSOP%7C411-17635%7CAMSYNCS%7C; check=true; s_cc=true; _parsely_visitor={%22id%22:%22781f088f-4779-41bf-9266-a7b79a0d399c%22%2C%22session_count%22:29%2C%22last_session_ts%22:1523136174779}; _gid=GA1.2.1824515317.1523324029; ak_bmsc=FC6D19012F82D0D18D317FE868EAEC686011469B111D00007817CC5A9663AA1F~pl9Gh+TED93URpiqeZkD681KhC9odzuoxqSR3lSOos6+2UhxfJvCFGQcjcNU3G7zt1ykNRSoa6um4SHe2uoMUm/DJieIxSPMdc6ydKe2wJUq0FenRm13r5WoYxo78AtRGcAFQ6dYoiKqTtpWHclBBM3ThywQRowNnCKGsvqcNLDy48T22cgEcU3+hTAPf/Y5F8gBXWEZmOJAH8JUkyrsyD1bkG+cO9IPMjQr9FkVbdqrI=; _gat=1; ugs=1; mbox=PC#e6df7796c63149b29287d11e3fc051ad.28_14#1584394276|session#7dcc805c39f9407c8b416943ff86c20f#1523326682; bm_sv=C13F5B719CDFD7C8A25B486915E24CC5~N3dAJlViEU3FkMoYoNgo7u6Ll4KW/1fnfPv8ari22+B1S6dgk9tbK5Qsm4fcZl8rPc/WEj9AYxSCsAU4rEQgn3QZzLtZYRHsIykdpZqMgRfYbkNrchhwBjhn4T2NMDH8TnfWjPbVp7boqaDvnWoeEg==; s_sq=%5B%5BB%5D%5D'
        }
        response = requests.get(url, headers=header, timeout=10)
        data = response.json()['resultSets'][0]['rowSet']
        print("using API")
    except requests.ReadTimeout:
        print("unable to reach API, so using old json")
        data = json.load(open(per36_json))['resultSets'][0]['rowSet']

    index = 0
    print("grabbing nba per 36")

    for row in data:
        min = row[9]
        if min < 300:
            continue
        id = str(row[0])
        name = str(row[1])
        teamID = str(row[2])
        team = str(row[3])
        with open(pace_csv, 'r') as pace_file:
            rows = csv.reader(pace_file, delimiter=",")
            next(rows, None)
            for t in rows:
                if teamID == t[0]:
                    pace = t[1]
                    break

        gp = str(row[5])
        min = str(min)
        pts = str(float(row[29]) * (avg_pace/float(pace)))
        reb = str(float(row[21]) * (avg_pace/float(pace)))
        ast = str(float(row[22]) * (avg_pace/float(pace)))
        stl = str(float(row[24]) * (avg_pace/float(pace)))
        blk = str(float(row[25]) * (avg_pace/float(pace)))
        tov = str(float(row[23]) * (avg_pace/float(pace)))
        fgper = str(float(row[12]) * (avg_pace/float(pace)))
        threeper = str(float(row[15]) * (avg_pace/float(pace)))
        ftper = str(float(row[18]) * (avg_pace/float(pace)))

        print("writing row for player " + id)
        nba_36.write(str(index) + "," + id + "," + name + "," + teamID + "," + team + "," + gp + "," + min + "," + pts+ "," + reb + "," +
                     ast + "," + stl + "," + blk + "," + tov + "," + fgper + "," + threeper + "," + ftper + "\n")
        index += 1
    nba_36.close()

    return True


done = False
while not done:
    done = scrape()
