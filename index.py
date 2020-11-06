import json
from flask import Flask
from flask import render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail

from libs.handler import http_handler
from libs.mail import send_mail

app = Flask(__name__)

app.config.from_pyfile('config.py')
mail = Mail(app)

scheduler = BackgroundScheduler()
scheduler.start()


@app.route('/')
def index():
    with open('server.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    status(data)
    with open('server.json', 'r') as f:
        datas = json.load(f)
    return render_template('index.html', datas=datas)

def status(data):
    for task in data['tasks']:
        status = http_handler(task['address'])
        if status != task['status'] and status=='在线':
            task['status'] = status
            with open('server.json', 'w', encoding='utf-8') as f:
                json.dump(data,f)
        if status != task['status'] and status =='异常':
            task['status'] = status
            with open('server.json', 'w', encoding='utf-8') as f:
                json.dump(data,f)
            send_mail(app,task['owner'],task['address'])
    return data

@scheduler.scheduled_job('interval',id='online_check',seconds=10)
def online_check():
    with open('server.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    status(data)

if __name__ == '__main__':
    app.run()