#!/usr/bin/python
import os
from celery.result import AsyncResult
from flask import Flask
from flask import redirect
from flask import request
from flask import render_template

from tasks import show_avg_id
from tasks import celery

from iron_celery import iron_cache_backend

app = Flask(__name__)

# ironmq://project_id:token@
IRONURL = os.environ['IRONURL']
APIKEY = os.environ['STEAMAPI']

#backend = iron_cache_backend.IronCacheBackend('ironcache://'+IRONURL)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/queue', methods=['POST'])
def runTask():
    res = show_avg_id.delay(request.form['id'])
    return redirect('/id/'+res.id)

@app.route('/id/<steamid>')
def show_avg(steamid):
    result = AsyncResult(steamid, app=celery)
    print result
    print result.ready()
    if result.ready():
        return render_template('avg.html', avg=result.get())
    elif result.failed():
        return result.traceback
    else:
        return render_template('processing.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
