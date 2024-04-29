#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-09-19
@FilePath    :  __init__.py
@FileVersion :  1.0
@LastEditTime:  2023-09-19
@FileDesc    :  提供该文件夹的全局模块导出
'''

import logging
import traceback
import os
import sys
import time
import datetime

ROOTPATH = r'/www/wwwroot/Dingtalk-MonitorBook/'
if os.path.join(ROOTPATH, 'src') not in sys.path:
    sys.path.append(os.path.join(ROOTPATH, 'src'))

from utils.utils_logging import CustomLogger
