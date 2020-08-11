import urllib.request
import requests
import re
from bs4 import BeautifulSoup
import csv
import datetime
from PIL import Image

fields = ['ARTIST', 'DATE', 'MONTH', 'EVENT',
          'FACEBOOK', 'LIVESTREAM', 'GENRE']

current_time = datetime.datetime.now()

filename = str(current_time.date())+".csv"

response = requests.get(
    'https://www.bandsintown.com/?came_from=257&hide_homepage=true&sort_by_filter=Number+of+RSVPs')

bs = BeautifulSoup(response.text, 'html.parser')
divs = bs.findAll(class_='_2gFU0t87uCmml36Fna9lZu')

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

    for div in divs:
        linke = []
        Artist = div.findChild(class_='_30guAjxdBy0Pk99zTF_aFt').get_text()
        date = div.findChild(class_='_1XNZaAvcDTPpSbzcoV0W3n').get_text()
        month = div.findChild(class_='_3kalOIVEhJHQXgHatFoDeJ').get_text()
        event = str(div.findChild(
            class_='_1iWvR5fnY_ZywNOmtcS95E').get_text())
        time = div.findChild(class_='_3RH1_pJ5HhrUeNswZyf8r5').get_text()
        linke.append(Artist)
        linke.append(date)
        linke.append(month)
        linke.append(event)

        response_each = requests.get(div.findChild(
            class_='_3buUBPWBhUz9KBQqgXm-gf').find_next('a')['href'])

        bs2 = BeautifulSoup(response_each.text, 'html.parser')

    # Image download part
        img2 = bs2.findChild(class_='_3FxoLllHIYDsTLMcW1mAl8')
        if img2:
            imag = bs2.findChild(
                class_='_3FxoLllHIYDsTLMcW1mAl8').find_next('img')['src']
            img = Image.open(requests.get(str(imag), stream=True).raw)
            # urllib.request.urlretrieve(imag, event+".jpg")
            img.save(str(event).replace(
                "/", "_").replace("&", "_").replace(":", "_").replace('"', "-")+'.jpg')

        fb2 = bs2.find('div', class_='_3EAC_52CXB3SEGlNmW1zZM')
    # FACEBOOK
        if fb2:
            fb = bs2.findChild(class_='_3EAC_52CXB3SEGlNmW1zZM').find_next(
                'a', href=re.compile('facebook'))['href']
            print('Facebook : ' + fb)
            linke.append(fb)
        else:
            linke.append("")
        ls2 = bs2.find('div', class_='Wla7qETMG4RlwfQQMTIqx')
    # LIVESTREAM
        if ls2:
            ls = bs2.findChild(
                class_='Wla7qETMG4RlwfQQMTIqx').find_next('a')['href']
            print('Livestream : ' + ls)
            linke.append(ls)
        else:
            linke.append("")

        genre = bs2.findChild(class_='_1v6hYzlTV-hB2ZkAb6CiCv').get_text()
        linke.append(genre)
        print("Artist : "+Artist+"\n"
              + "Date : "+date, month+"\n"
              + "Event : "+event+"\n"
              + "Time : "+time+"\n"
              + "Genre : "+genre)

        # writing the fields
        csvwriter.writerow(linke)
