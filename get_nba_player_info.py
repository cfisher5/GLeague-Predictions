import requests
import os
import json
import pandas as pd


wd = os.getcwd()

if wd == "/home/cfisher5":
    csv_filename = "GLeague-Predictions/data/nba_player_data.csv"
    per_36 = "GLeague-Predictions/data/nba36.csv"
    merge_filename = "GLeague-Predictions/data/nba_merge.csv"
    nba_data = "GLeague-Predictions/data/nba_player_data.csv"
    active_json = "GLeague-Predictions/data/activeplayers.json"

else:
    csv_filename = "data/nba_player_data.csv"
    per_36 = "data/nba36.csv"
    merge_filename = "data/nba_merge.csv"
    nba_data = "data/nba_player_data.csv"
    active_json = "data/activeplayers.json"


def scrape():

    nba_data = open(csv_filename, 'w')
    nba_data.write('ID,height,height_inches,weight,pos\n')
    url = "http://www.nba.com/players/active_players.json"
    try:
        header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                  'Dnt': '1',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'en-US',
                  'Host': 'stats.nba.com',
                  'Referer': 'http://stats.nba.com/players/bio/',
                  'Connection': 'keep-alive',
                  'Cookie': '__qca=P0-1808023843-1509330139519; __gads=ID=d2f2596bbb58f01c:T=1509330139:S=ALNI_MaT7n-b9IBB-xvB8pcKOaJC1BkUAQ; _privy_6A673486582982E68B43A020=%7B%22uuid%22%3A%2228a3d7ad-6f73-4ec9-b8e1-4cf5ef2ae0a7%22%2C%22variations%22%3A%7B%7D%2C%22country_code%22%3A%22US%22%7D; optimizelyEndUserId=oeu1511727268075r0.8663817233978857; optimizelyBuckets=%7B%7D; _mkto_trk=id:167-EIT-370&token:_mch-nba.com-1511727269937-39500; _ga=GA1.2.54571634.1509384958; s_fid=3FF52C8893D8DC3F-0876B27F6DC9308A; s_vi=[CS]v1|2CFB466F05033209-400011842000267A[CE]; optimizelySegments=%7B%222704480408%22%3A%22none%22%2C%222707460365%22%3A%22gc%22%2C%222708140383%22%3A%22false%22%2C%222708290386%22%3A%22search%22%2C%223713124431%22%3A%22gc%22%2C%223728264737%22%3A%22search%22%2C%223734713784%22%3A%22false%22%2C%223735704323%22%3A%22none%22%7D; _privy_a=%7B%22referring_domain%22%3A%22gleague.nba.com%22%2C%22referring_url%22%3A%22http%3A%2F%2Fgleague.nba.com%2Fgames%2F20171118%2FLAKRAP%2F%22%2C%22utm_medium%22%3A%22unknown%22%2C%22utm_source%22%3Anull%2C%22search_term%22%3Anull%2C%22initial_url%22%3A%22http%3A%2F%2Flakeland.gleague.nba.com%2F%22%2C%22sessions_count%22%3A2%2C%22pages_viewed%22%3A3%7D; __unam=b2ed6e-15fcdf3d2f5-4b3ade60-3; AMCV_248F210755B762187F000101%40AdobeOrg=-1891778711%7CMCAID%7C2CFB466F05033209-400011842000267A%7CMCIDTS%7C17580%7CMCMID%7C68373101399095200423489720217121077769%7CMCAAMLH-1519514718%7C7%7CMCAAMB-1519514718%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1518917118s%7CNONE%7CMCSYNCSOP%7C411-17587%7CvVersion%7C2.4.0; aam_uuid=68398756077489532373486601900571739190; __insp_wid=954630821; __insp_slim=1521945122677; __insp_nv=true; __insp_targlpu=aHR0cDovL3d3dy5uYmEuY29tL3JhcHRvcnMvd2F5bmUtZW1icnktZmVsbG93c2hpcC8%3D; __insp_targlpt=VGhlIFdheW5lIEVtYnJ5IEZlbGxvd3NoaXAgfCBUb3JvbnRvIFJhcHRvcnM%3D; __insp_norec_sess=true; ug=5a4f2f0205fde10a3c26e1057b001fb4; AAMC_nba_0=REGION%7C9%7CAMSYNCSOP%7C411-17635%7CAMSYNCS%7C; check=true; s_cc=true; _gid=GA1.2.1824515317.1523324029; ak_bmsc=FC6D19012F82D0D18D317FE868EAEC686011469B111D00007817CC5A9663AA1F~pl9Gh+TED93URpiqeZkD681KhC9odzuoxqSR3lSOos6+2UhxfJvCFGQcjcNU3G7zt1ykNRSoa6um4SHe2uoMUm/DJieIxSPMdc6ydKe2wJUq0FenRm13r5WoYxo78AtRGcAFQ6dYoiKqTtpWHclBBM3ThywQRowNnCKGsvqcNLDy48T22cgEcU3+hTAPf/Y5F8gBXWEZmOJAH8JUkyrsyD1bkG+cO9IPMjQr9FkVbdqrI=; ugs=1; _parsely_session={%22sid%22:30%2C%22surl%22:%22http://www.nba.com/kings/roster/bruno-caboclo%22%2C%22sref%22:%22https://www.google.com/%22%2C%22sts%22:1523325490628%2C%22slts%22:1523136174779}; _parsely_visitor={%22id%22:%22781f088f-4779-41bf-9266-a7b79a0d399c%22%2C%22session_count%22:30%2C%22last_session_ts%22:1523325490628}; s_sq=%5B%5BB%5D%5D; bm_sv=C13F5B719CDFD7C8A25B486915E24CC5~N3dAJlViEU3FkMoYoNgo7u6Ll4KW/1fnfPv8ari22+B1S6dgk9tbK5Qsm4fcZl8rPc/WEj9AYxSCsAU4rEQgn3QZzLtZYRHsIykdpZqMgRe3B1i2+cAKZjuYHRgfXensQwRodohhp/TCL9PbMAfl3A==; _gat=1; mbox=PC#e6df7796c63149b29287d11e3fc051ad.28_14#1584394276|session#7dcc805c39f9407c8b416943ff86c20f#1523327462'
                  }
        response = requests.get(url, headers=header, timeout=10)
        data = response.json()

    except Exception:
        print("unable to reach API so using old json")
        data = json.load(open(active_json))

    for row in data:
        id = str(row['personId'])
        height = str(row['heightFeet']) + "-" + str(row['heightInches'])
        try:
            height_inches = int(row['heightFeet']) * 12 + int(row['heightInches'])
            weight = str(row['weightPounds'])
            pos = row['posExpanded']
            nba_data.write(id + "," + height + "," + str(height_inches) + "," + weight + "," + pos + "\n")
        except ValueError:
            print("player " + id + " does not have height listed. excluding him.")
            continue

    nba_data.close()
    return True


done = scrape()
data = pd.read_csv(per_36, sep=",")
data = data[['ID', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGper', 'threeper', 'FTper']]
height_weight_data = pd.read_csv(nba_data, sep=",")
height_weight_data = height_weight_data[['ID', 'height_inches', 'weight']]

merge = pd.merge(left=data, right=height_weight_data, how='inner', on='ID')
merge.to_csv(merge_filename)
merged = merge.drop('ID', axis=1)
