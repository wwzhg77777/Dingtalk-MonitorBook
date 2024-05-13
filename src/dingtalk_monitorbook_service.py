#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-07-18 15:00:00
@FilePath    :  dingtalk_monitorbook_service.py
@FileVersion :  1.1
@LastEditTime:  2023-08-23
@FileDesc    :  API接口服务: 接收钉钉的事件订阅数据
'''

import os
import sys

from flask import Flask, Response, request
from dingtalkchatbot.chatbot import DingtalkChatbot

from getCallBack import getCallBack
from api.getData import getData
from components.DingtalkOpenAPI import DingtalkOpenAPI
from components.LocalOpenAPI import LocalOpenAPI
from utils.utils_config import DD_CONFIG_CALLBACK_0001
from utils.utils_const import CONST, DD_CONST
from utils.utils_logging import CustomLogger

if os.path.join(CONST.ROOTPATH, 'src') not in sys.path:
    sys.path.append(os.path.join(CONST.ROOTPATH, 'src'))

logger_hander = CustomLogger(log_name_='dd_callback', log_desc_='monitor-book', is_console_=False, start_in_log_=True)
logger = logger_hander.get_logs()

app = Flask(__name__)
resp_headers = {
    'Access-Control-Allow-Credentials': 'false',
    'Access-Control-Allow-Headers': 'Content-Type,X-Requested-with',
    'Access-Control-Allow-Origin': 'https://oabook-monitor.uwellit.com',
}

ding_api = DingtalkOpenAPI(app_key_=DD_CONST.APP_KEY, app_secret_=DD_CONST.APP_SECRET, g_api_uri_host_=DD_CONST.API_URI_HOST)
local_api = LocalOpenAPI(access_token_=CONST.API_TOKEN, g_api_uri_host_=CONST.API_URI_HOST)
secret = DD_CONFIG_CALLBACK_0001.groupChat_robot_webhook_secret
webhook = DD_CONFIG_CALLBACK_0001.groupChat_robot_webhook_link
robot = DingtalkChatbot(webhook=webhook, secret=secret)


@app.route('/getCallBack', methods=['POST', 'OPTIONS'])
def resp_getCallBack():
    resp_headers['Access-Control-Allow-Methods'] = 'POST OPTIONS'
    callback = getCallBack(CONST.ROOTPATH, request, logger, ding_api=ding_api,local_api=local_api, robot=robot)
    if callback:
        return Response(callback, mimetype='application/json', headers=resp_headers)
    else:
        return ''


@app.route('/getData', methods=['GET', 'OPTIONS'])
def resp_getData():
    resp_headers['Access-Control-Allow-Methods'] = 'GET OPTIONS'
    resp = Response(getData(CONST.ROOTPATH, request), mimetype='application/json', headers=resp_headers)
    return resp


if __name__ == '__main__':
    app.run(host=CONST.SERVICE_URI_HOST, port=CONST.SERVICE_URI_POST)  # release
    # app.run(host=CONST.SERVICE_URI_HOST, port=CONST.SERVICE_URI_POST, debug=True, use_reloader=False)  # debug
    # app.run(host=CONST.SERVICE_URI_HOST, port=CONST.SERVICE_URI_POST, debug=True)  # debug
