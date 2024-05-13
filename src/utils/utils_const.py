#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-09-19
@FilePath    :  utils_const.py
@FileVersion :  1.1
@LastEditTime:  2023-09-19
@FileDesc    :  记录固定的常数值
'''


class CONST:
    '''
    应用程序的常量表
    '''

    ROOTPATH = r'/www/wwwroot/Dingtalk-MonitorBook/'
    '''应用程序的根目录'''

    WEB_URI_SCHEME = 'https'
    '''HTTP协议簇'''

    SERVICE_URI_POST = 8000
    '''nginx服务器的web站点监听端口'''

    SERVICE_URI_HOST = '0.0.0.0'
    '''nginx服务器的主机名称'''

    WEB_URI_HOST = 'monitor-book.mysite.com'
    '''web站点的主机名称'''

    API_URI_HOST = 'localapi.mysite.com'
    '''本地中间件API的请求Host名称'''

    API_TOKEN: str = 'your_localapi_token'
    '''本地中间件API请求Header头的Token'''


class DD_CONST:
    '''
    关联钉钉企业内部应用Api接口的常量表
    '''

    API_URI_HOST = 'api.dingtalk.com'
    '''钉钉API的请求Host名称'''

    APP_KEY: str = 'your_app_key'
    '''钉钉应用的AppKey'''

    APP_SECRET: str = 'your_app_secret'
    '''钉钉应用的AppSecret'''

    APP_TOKEN: str = 'your_app_token'
    '''钉钉应用, 事件与回调: 加密aes_key'''

    APP_AESKEY: str = 'your_app_aeskey'
    '''钉钉应用, 事件与回调: 签名token'''

    DING_ACTION_URL = 'dingtalk://dingtalkclient/action/openapp'
    '''钉钉聊天窗口跳转工作台的url'''

    DING_PAGELINK_URL = 'dingtalk://dingtalkclient/page/link'
    '''钉钉聊天窗口打开第三方链接的url, 可选在窗口侧边栏打开或外部浏览器打开'''
