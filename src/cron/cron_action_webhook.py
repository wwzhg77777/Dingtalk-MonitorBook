#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2024-02-18
@FilePath    :  cron_action_webhook.py
@FileVersion :  1.0
@LastEditTime:  2024-02-18
@FileDesc    :  cron定时任务: 每天 12点03分 , 18点03分. 定时执行数据库记录和钉钉群聊通讯录变更告警推送
'''

import os
import sys
import json
import datetime
from collections import Counter
from urllib.parse import quote
from dingtalkchatbot.chatbot import DingtalkChatbot

ROOTPATH = r'/www/wwwroot/Dingtalk-MonitorBook/'

if os.path.join(ROOTPATH, 'src') not in sys.path:
    sys.path.append(os.path.join(ROOTPATH, 'src'))

from components.MySQLHandle import MySQLHandle
from utils.utils_config import DD_CONFIG_CALLBACK_0001
from utils.utils_const import CONST, DD_CONST

# 定时执行数据库记录和钉钉群聊通讯录变更告警推送
if __name__ == '__main__':
    nowtime = datetime.datetime.now()
    try:
        webhook = DD_CONFIG_CALLBACK_0001.groupChat_robot_webhook_link
        secret = DD_CONFIG_CALLBACK_0001.groupChat_robot_webhook_secret
        robot = DingtalkChatbot(webhook=webhook, secret=secret)
        sql_handle = MySQLHandle()
        sql_handle.connect()

        before_stime = nowtime + datetime.timedelta(hours=-18 if nowtime.hour == 12 else -6)
        cron_msg_title = '钉钉通讯录的变更告警推送'
        cron_msg = ''
        cron_msg += f"#### **{cron_msg_title}**  \n\n  "
        cron_msg += f"<font color=\"#0000FF\">**时间：{before_stime.strftime('%Y年%m月%d日 %H:%M:%S')} 至 {nowtime.strftime('%Y年%m月%d日 %H:%M:%S')}**</font>  \n\n  "

        select_sql = f"SELECT * FROM `monitor_book_logs` WHERE `time` BETWEEN '{before_stime.strftime('%Y-%m-%d %H:%M:%S')}' AND '{nowtime.strftime('%Y-%m-%d %H:%M:%S')}'"
        json_data = sql_handle.execute(select_sql)
        json_data = [{'eventtype': v[1], 'eventtitle': v[2], 'time': v[3], 'data': json.loads(v[4]), 'item': json.loads(v[5])} for v in json_data]

        if len(json_data) > 0:
            redirect_urlencode = quote(f"{CONST.WEB_URI_SCHEME}://{CONST.WEB_URI_HOST}/?type=search&getall=false&stime={before_stime.strftime('%Y-%m-%d %H')}&etime={nowtime.strftime('%Y-%m-%d %H')}")
            dingtalk_jump_url = f"{DD_CONST.DING_PAGELINK_URL}?url={redirect_urlencode}&pc_slide=false"
            for title, count in Counter([v['eventtitle'] for v in json_data]).items():
                if title in ['企业增加员工', '企业员工离职']:
                    for val in [f"[{item['time']}] {v['name']}({v['id']})" for item in json_data if item['eventtitle'] == title for v in item['data']]:
                        cron_msg += f"- **{title}: {val}**  \n\n  "
                else:
                    cron_msg += f"- **{title} 次数：{count}**  \n\n  "

            cron_msg += f"**[查看详情日志]({dingtalk_jump_url})**  \n\n  "
        else:
            cron_msg += f"**无日志产生**  \n\n  "

        robot.send_markdown(title=cron_msg_title, text=cron_msg, is_at_all=False)
        sql_handle.close_conn()
    except Exception as e:
        open(os.path.join(CONST.ROOTPATH, 'src', 'static', 'err.log'), 'a+', encoding='utf-8').writelines(str(e))
