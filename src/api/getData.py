#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2024-01-29
@FilePath    :  getData.py
@FileVersion :  1.0
@LastEditTime:  2024-01-29
@FileDesc    :  API接口: 获取IDaaS系统的待同步数据
'''

import os
import sys
import json
from flask import Request
from components.MySQLHandle import MySQLHandle

ROOTPATH = r'/www/wwwroot/Dingtalk-MonitorBook/'
if os.path.join(ROOTPATH, 'src') not in sys.path:
    sys.path.append(os.path.join(ROOTPATH, 'src'))


def getData(rootpath_: str, request_: Request = None):
    '''
        数据同步页面, 获取对比后的差异数据集
        rootpath_   : 当前项目的根目录
        request_    : 客户端的请求体request内容

    SUCCESS
    return dict     : 成功返回 dict对象, json格式

    ERROR
    return False    : 错误返回 False
    '''
    result = {'code': 0, 'msg': '', 'count': 0, 'data': {}}
    token = request_.args.get('token', default='')
    mode = request_.args.get('mode', default='')
    page = request_.args.get('page', default='')
    limit = request_.args.get('limit', default='')

    stime = request_.args.get('stime', default='')
    etime = request_.args.get('etime', default='')
    getall = request_.args.get('getall', default='')
    if token == '' and mode != 'get_data' or page == '' or limit == '':
        result['code'] = 4001000
        result['msg'] = '格式错误'
        return json.dumps(result, ensure_ascii=False)
    if getall == 'false' and (not stime.startswith('20') or not etime.startswith('20') or len(stime) != 13 or len(etime) != 13):
        result['code'] = 4001001
        result['msg'] = '格式错误'
        return json.dumps(result, ensure_ascii=False)
    if rootpath_ not in sys.path:
        sys.path.append(rootpath_)

    sql_handle = MySQLHandle()
    sql_handle.connect()
    if getall == 'true':
        select_sql = f"SELECT * FROM `monitor_book_logs` ORDER BY `time` DESC"
    else:
        select_sql = f"SELECT * FROM `monitor_book_logs` WHERE `time` BETWEEN '{stime}:03:00' AND '{etime}:03:00'"

    json_data = sql_handle.execute(select_sql)
    json_data = [{'eventtype': v[1], 'eventtitle': v[2], 'time': v[3], 'data': json.loads(v[4]), 'item': json.loads(v[5])} for v in json_data]
    page = int(page)
    limit = int(limit)
    ret_data = json_data[(page - 1) * limit : page * limit]
    sql_handle.close_conn()

    result['data'] = ret_data
    result['count'] = len(json_data)
    result['msg'] = 'success.'
    return json.dumps(result, ensure_ascii=False)
