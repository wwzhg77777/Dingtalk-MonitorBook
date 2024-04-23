#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-09-19
@FilePath    :  utils_func.py
@FileVersion :  1.2
@LastEditTime:  2023-09-19
@FileDesc    :  提供自定义的工具函数
'''

import json
from . import *
from datetime import datetime
from dingtalkchatbot.chatbot import DingtalkChatbot


def loop_json2dict(source_item: object):
    '''
    递归处理, 将dict里边包含json字符串的值都转换成python的dict类型
    '''
    if type(source_item) == dict:
        for k, v in source_item.items():
            if type(v) == dict or type(v) == list:
                loop_json2dict(source_item[k])
            else:
                try:
                    source_item[k] = str(source_item[k]).replace('\r', '\\r').replace('\n', '\\n')
                    source_item[k] = json.loads(str(source_item[k]), strict=False)
                    if type(source_item[k]) == dict or type(source_item[k]) == list:
                        loop_json2dict(source_item[k])
                except ValueError:
                    pass
    elif type(source_item) == list:
        for _j in range(len(source_item)):
            if type(source_item[_j]) == dict or type(source_item[_j]) == list:
                loop_json2dict(source_item[_j])
            else:
                try:
                    source_item[_j] = str(source_item[_j]).replace('\r', '\\r').replace('\n', '\\n')
                    source_item[_j] = json.loads(str(source_item[_j]), strict=False)
                    if type(source_item[_j]) == dict or type(source_item[_j]) == list:
                        loop_json2dict(source_item[_j])
                except ValueError:
                    pass


def unix2formatTime(_unix: int = time.time(), _formatStr: str = '%Y-%m-%d %H:%M:%S', _isUnit10: bool = True):
    if _isUnit10:
        return time.strftime(_formatStr, time.localtime(int(_unix)))
    else:
        return datetime.fromtimestamp(float(_unix) / 1000).strftime(_formatStr)


def utc2unix10Time(_utc_formatStr: str, _formatStr: str = '%Y-%m-%dT%H:%MZ'):
    return int(time.mktime(time.strptime(_utc_formatStr, _formatStr)))


def utc2unix13Time(_utc_formatStr: str, _formatStr: str = '%Y-%m-%dT%H:%MZ'):
    return int(f"{int(time.mktime(time.strptime(_utc_formatStr, _formatStr))):<013d}")
