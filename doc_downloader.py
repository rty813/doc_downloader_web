#!/usr/local/bin/python3.7
from flask import Flask, request, render_template, flash, send_from_directory, jsonify, url_for
import sys
import os
import time
from celery import Celery
import docDownloader
import random
os.chdir("/var/www/doc_downloader/")
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 配置消息代理的路径，如果是在远程服务器上，则配置远程服务器中redis的URL
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# 要存储 Celery 任务的状态或运行结果时就必须要配置
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# 初始化Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# 将Flask中的配置直接传递给Celery
celery.conf.update(app.config)

@celery.task(bind=True)
def long_task(self, url):
    def callback(current, total, message):
        self.update_state(state='PROGRESS', meta={'current': current, 'total': total, 'status': message})

    res = docDownloader.download(url, callback)
    if not res[0]:
        return {'current': 0, 'total': 100, 'status': '下载失败', 'result': res[1]}
    else:
        return {'current': 100, 'total': 100, 'status': '下载成功', 'result': res[1]}
    # return send_from_directory('output', res[1] + ".pdf", as_attachment=True)

# @app.route('/', methods=('GET', 'POST'))
# def download():
#     return render_template('index.html')

@app.route('/longtask', methods=['POST'])
def longtask():
    if request.method == 'POST':
        url = request.form['url']
        task = long_task.delay(url)
        return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING': # 在等待
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE': # 没有失败
        response = {
            'state': task.state, # 状态
            # meta中的数据，通过task.info.get()可以获得
            'current': task.info.get('current', 0), # 当前循环进度
            'total': task.info.get('total', 1), # 总循环进度
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # 后端执行任务出现了一些问题
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': str(task.info), # 报错的具体异常
        }
    return jsonify(response)


@app.route('/')
def test():
    return render_template('download.html')

@app.route('/file', methods=['GET'])
def file():
    return send_from_directory('output', request.args.get('name', '') + ".pdf", as_attachment=True)