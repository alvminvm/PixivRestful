from flask import Flask
from flask import request
from pixivpy3 import AppPixivAPI
from functools import lru_cache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
pixiv = AppPixivAPI()
pixiv.set_accept_language("zh-cn")

@app.route("/login")
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    return pixiv.login(username, password)

@app.route("/refresh_auth")
def refresh_auth():
    return pixiv.auth()

@app.route("/illust/<id>")
def illust(id):
    return get_illust_detail_with_cache(id)

@lru_cache()
def get_illust_detail_with_cache(id):
    print("get detail")
    return pixiv.illust_detail(id)

def refresh_auth_job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -> refresh auth")
    result = pixiv.auth()
    print(result)

def start_job():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(refresh_auth_job, 'interval', seconds=5)
    scheduler.add_job(refresh_auth_job, 'interval', minutes=50)
    scheduler.start()

if __name__ == '__main__':

    start_job()

    app.run()
