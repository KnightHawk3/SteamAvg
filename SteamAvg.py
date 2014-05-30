#!/usr/bin/python
import requests
import json
import os

APIURL = 'http://api.steampowered.com'
APIKEY = os.environ['STEAMAPI'] # Import api key from environment variables

steamid = 76561198025500278 # Melodys
steamid = 76561198019392997 # LHC's

def urlify(url):
    url = url.replace(" ", "-")
    url = url.strip(":")
    return url.lower()

r = requests.get(APIURL + '/IPlayerService/GetOwnedGames/v0001/?key=' + APIKEY + '&steamid=' + str(steamid) + '&format=json&include_appinfo=1')

data = json.loads(r.text)

scores = []

for game in data['response']['games']:
    gameurl = urlify(game['name'])
    try:
        score = int(requests.get('http://www.metacritic.com/game/pc/' + gameurl ).text.split('<span itemprop="ratingValue">')[1].split('</span>')[0])
        scores.append(score)
    except IndexError:
        pass

print sum(scores)/len(scores)
print  str(len(scores)) + " out of " + str(len(data['response']['games'])) + " results sampled."
