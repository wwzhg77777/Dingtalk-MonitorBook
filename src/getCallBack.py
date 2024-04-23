#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-09-19
@FilePath    :  getCallBack.py
@FileVersion :  1.0
@LastEditTime:  2023-09-19
@FileDesc    :  API接口: 接收钉钉的事件订阅数据
'''

import json
import os
import sys
import logging
import traceback
from flask import Request

from api.callback_0001 import callback_0001
from components.DingCallbackCrypto3 import DingCallbackCrypto3
from utils.utils_config import *
from utils.utils_func import unix2formatTime
from utils.utils_const import DD_CONST
from utils.utils_logging import CustomLogger


def instance_log_in_local(rootpath_: str, dd_msg: str, logger_: logging.Logger, dec: str):
    '''
    实例的n次回调只处理一次
    '''
    if os.path.exists(os.path.join(rootpath_, 'src', 'temp', f"{dd_msg['TimeStamp']}_{dd_msg['EventType']}")):
        return True
    with open(os.path.join(rootpath_, 'src', 'temp', f"{dd_msg['TimeStamp']}_{dd_msg['EventType']}"), 'w', encoding='utf-8') as f:
        f.writelines(f"[{unix2formatTime(dd_msg['TimeStamp'],'%Y-%m-%d %H:%M:%S.%f',False)[:-3]}]\tcurrent state: start\r\n")
    logger_.info('not reply. decrypt data: {}'.format(dec))  # 记录info日志到文件
    return False


def getCallBack(rootpath_: str, request_: Request = None, logger_: CustomLogger = None, *args, **kwargs):
    '''
        接收钉钉的事件订阅数据, 判断是否返回响应数据
        rootpath_   : 当前项目的根目录
        request_    : 客户端的请求体request内容
        *args       : 不定参数集. list列表允许输入多个参数
        **kwargs    : 不定参数集. dict集合允许输入多个键值对

    SUCCESS
    return str|None : 响应时返回 str字符串, json序列化数据; 无需响应时无需return; 未正确匹配时return None

    ERROR
    return False    : 错误返回 False
    '''

    if os.path.join(rootpath_, 'src') not in sys.path:
        sys.path.append(os.path.join(rootpath_, 'src'))
    signature = request_.args.get('signature')
    msg_signature = request_.args.get('msg_signature')
    timestamp = request_.args.get('timestamp')
    nonce = request_.args.get('nonce')
    encrypt = request_.json['encrypt']
    print(f"request.args::: {request_.args}") if DD_CONFIG_GLOBAL.debug_print_flag == 2 else ''
    print(f"request.data::: {request_.data}") if DD_CONFIG_GLOBAL.debug_print_flag == 2 else ''
    print(f"request.form::: {request_.form}") if DD_CONFIG_GLOBAL.debug_print_flag == 2 else ''
    print(f"request.json::: {request_.json}") if DD_CONFIG_GLOBAL.debug_print_flag == 2 else ''
    print(f"signature: {signature}\nmsg_signature: {msg_signature}\ntimestamp: {timestamp}\nnonce: {nonce}\nencrypt: {encrypt}\n") if DD_CONFIG_GLOBAL.debug_print_flag == 1 else ''

    dingCrypto = DingCallbackCrypto3(DD_CONST.APP_TOKEN, DD_CONST.APP_AESKEY, DD_CONST.APP_KEY)
    dec = dingCrypto.getDecryptMsg(signature, timestamp, nonce, encrypt)
    if dec == '{"EventType":"check_url"}':
        logger_.info('reply. decrypt data: {}'.format(dec))
        enc = dingCrypto.getEncryptedMap('success')
        result = {'msg_signature': enc['msg_signature'], 'timeStamp': enc['timeStamp'], 'nonce': enc['nonce'], 'encrypt': enc['encrypt']}
        return json.dumps(result, ensure_ascii=False)
    elif dec is not None:
        try:
            dd_msg = json.loads(dec)
            if 'dict' not in str(type(dd_msg)):
                return

            ################ 此处开始自定义代码 ################
            if dd_msg['EventType'] in DD_CONFIG_GLOBAL.subscribe_events:
                if instance_log_in_local(rootpath_, dd_msg, logger_, dec):
                    return  # 实例的n次回调只处理一次
                callback_0001(rootpath_, dd_msg, kwargs)  # 钉钉通讯录变更告警-callback_0001

        except Exception as e:
            with open(os.path.join(rootpath_, 'assets', 'logs', 'error.log'), 'a', encoding='utf-8') as f:
                f.write(f"\nException Error: {e}\n")
                f.write(traceback.print_exc())
            return False
