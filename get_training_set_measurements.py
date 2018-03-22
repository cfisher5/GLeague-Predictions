from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen

with open('data/training_data2.csv','w') as newFile:
    newFileWriter = csv.writer(newFile)
    with open('data/training_data.csv', 'r') as training:
        rows = csv.reader(training, delimiter=",")
        next(rows, None)
        for row in rows:
            realgm_id = row[2]
            url = "https://basketball.realgm.com" + realgm_id
            page = urlopen(url)
            soup = BeautifulSoup(page, "html.parser")
            pdivs = soup.find('div', attrs={'class': 'profile-box'}).div.find('div', attrs={'class': 'half-column-left'}).findAll('p')
            for p in pdivs:
                try:
                    strongs = p.findAll('strong')
                    for strong in strongs:
                        if "Height" in strong.text:
                            height = p.text.split(" ")[1]
                            feet, inches = height.split("-")
                            height = int(feet) * 12 + int(inches)
                            print(height)
                            row.append(height)
                        if "Weight" in strong.text:
                            weight = p.text.split(" ")[4]
                            print(weight)
                            row.append(weight)
                except AttributeError:
                    pass
            newFileWriter.writerow(row)

# make sure to write header after, and change training_data2 to training_data