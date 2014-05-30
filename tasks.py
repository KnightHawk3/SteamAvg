from celery import Celery
import iron_celery
import json
import os
import celery

celery = Celery('tasks', broker='ironmq://', backend='ironcache://')

APIURL = 'http://api.steampowered.com'
APIKEY = os.environ['STEAMAPI'] # Import api key from environment variables

def urlify(url):
    url = url.replace(" ", "-")
    url = url.strip(":")
    return url.lower()

@celery.task()
def show_avg_id(steamid):
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
    avg = sum(scores)/len(scores)
    outof =  str(len(scores)) + " out of " + str(len(data['response']['games'])) + " results sampled."
    return avg + "<br>From " + outof

