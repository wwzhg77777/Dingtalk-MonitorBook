#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-08-23
@FilePath    :  cron_clear_tempfile.py
@FileVersion :  1.0
@LastEditTime:  2023-08-23
@FileDesc    :  cron定时任务: 每天04点00分. 定时清除早于当前时间的temp缓存文件
'''

import os
import sys
import time

ROOTPATH = r'/www/wwwroot/Dingtalk-MonitorBook/'

# 定时任务cron清除前一天的temp信息
if __name__ == '__main__':
    for tmpfname in [v for v in os.listdir(os.path.join(ROOTPATH, 'src', 'temp')) if '_' in v]:
        tmpfullfname = os.path.join(ROOTPATH, 'src', 'temp', tmpfname)
        os.remove(tmpfullfname)
