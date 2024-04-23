#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2024-01-02
@FilePath    :  DingtalkOpenAPI.py
@FileVersion :  1.0
@LastEditTime:  2024-01-02
@FileDesc    :  提供访问本地中间件API的工具函数
'''

import json

import requests
import urllib3

from . import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LocalOpenAPI:
    '''
    访问本地中间件的APIs接口数据, 本地服务报错不退出
    APIs:
    get_historyDingInfo         : 获取指定日期的钉钉通讯录数据
    get_historyUserInfo         : 从历史钉钉通讯录数据中查询指定用户
    get_historyDeptInfo         : 从历史钉钉通讯录数据中查询指定部门

    '''

    # Public var
    #
    jsonHeaders = {'Content-Type': 'application/json', 'Connection': 'close'}

    # Private var
    #
    __g_logger_info: logging.Logger
    # __g_logger_debug: logging.Logger
    __access_token: str
    '''请求本地中间件应用的Token'''
    __history_ding_data: dict
    '''从本地中间件API获取的钉钉通讯录数据'''
    __g_api_uri_host: str
    '''本地中间件API接口的host名称'''
    __is_log: bool
    '''是否记录info日志'''

    # 初始api接口
    def __init__(self, access_token_: str, g_api_uri_host_: str, is_log_: bool = True):
        '''
        构造函数:
        Load    : appKey, appSecret, Host
        '''
        self.__access_token = access_token_
        self.__g_api_uri_host = g_api_uri_host_
        self.__is_log = is_log_

        logger_hander_info = CustomLogger(log_name_='LocalOpenApi_info', is_console_=False, start_in_log_=False)
        self.__g_logger_info = logger_hander_info.get_logs()

    def set_headers(self, isHeaders: bool = True):
        '''
        补齐headers参数的token字段
        返回 json + tokens 的headers请求头
        '''
        sh_result = LocalOpenAPI.jsonHeaders
        if isHeaders:
            sh_result['token'] = self.__access_token
        return sh_result

    def get_historyDingInfo(self, api_uri_host_: str = 'localapi.mysite.com', api_uri_path_: str = '/u/meals/openApi/getMail', is_https: bool = True, *args, **kwargs):
        '''
        api     : 获取指定日期的钉钉通讯录数据
        url     : GET /getMail?date=String&type=Int32 HTTP/1.1
        host    : localapi.mysite.com
        Load    : ?kwargs['date', 'type']
        return  : (status_code:int, json:dict, onetime:time)
        '''
        get_historyDingInfo_result = ''
        _params = {}
        for k, v in kwargs.items():
            _params[k] = v
        try:
            _sT = time.time()
            _headers = self.set_headers()
            get_historyDingInfo_result = requests.get(url=f"{'https' if is_https else 'http'}://{api_uri_host_}{api_uri_path_}", params=_params, headers=_headers, verify=False)
            _oT = APITools.custom_random(str(time.time() - _sT), 3, 1)
            ret_json = get_historyDingInfo_result.json()
            if self.ret_error('get_historyDingInfo', get_historyDingInfo_result.status_code, ret_json):
                self.__g_logger_info.info('request Api[get_historyDingInfo] success. response msg: {}'.format(ret_json['msg'])) if self.__is_log else ''
                self.__history_ding_data = json.loads(ret_json['data'])
                return (ret_json, _oT)
        except Exception as e:
            self.__g_logger_info.error('localServerError: 接口请求参数异常, 检查[get_historyDingInfo]的入参. errmsg: {}.\n{}'.format(str(e), traceback.format_exc()))

    def get_historyUserInfo(self, *args, **kwargs):
        '''
        api     : 从历史钉钉通讯录数据中查询指定用户
        Load    : kwargs['userid']
        return  : json:dict
        '''

        def loop_get_dinginfo(each_item: list):
            for item_ in each_item:
                if item_['type'] == 1 and item_.__contains__('children') and len(item_['children']) > 0:
                    ret_json = loop_get_dinginfo(item_['children'])
                    if ret_json is not None:
                        return ret_json
                elif item_['type'] == 0 and item_['id'] == str(kwargs['userid']):
                    return item_

        try:
            self.get_historyDingInfo(date=str(datetime.date.today() + datetime.timedelta(days=-1)))
            if len(self.__history_ding_data) > 0:
                return loop_get_dinginfo(self.__history_ding_data)
        except Exception as e:
            self.__g_logger_info.error('localServerError: 接口请求参数异常, 检查[get_historyUserInfo]的入参. errmsg: {}.\n{}'.format(str(e), traceback.format_exc()))

    def get_historyDeptInfo(self, *args, **kwargs):
        '''
        api     : 从历史钉钉通讯录数据中查询指定部门
        Load    : kwargs['deptid']
        return  : json:dict
        '''

        def loop_get_dinginfo(each_item: list):
            for item_ in each_item:
                if item_['type'] == 1 and item_.__contains__('children') and len([v for v in item_['children'] if v['type'] == 1]) > 0:
                    ret_json = loop_get_dinginfo(item_['children'])
                    if ret_json is not None:
                        return ret_json
                elif item_['type'] == 1 and item_['id'] == str(kwargs['deptid']):
                    return item_

        try:
            self.get_historyDingInfo(date=str(datetime.date.today() + datetime.timedelta(days=-1)))
            if len(self.__history_ding_data) > 0:
                return loop_get_dinginfo(self.__history_ding_data)
        except Exception as e:
            self.__g_logger_info.error('localServerError: 接口请求参数异常, 检查[get_historyUserInfo]的入参. errmsg: {}.\n{}'.format(str(e), traceback.format_exc()))

    def ret_error(self, req_api_name_: str, req_status_code_: int, req_result_: object):
        '''
        根据本地中间件API文档的错误码, 记录错误日志到服务器, 不退出本地服务
        '''
        if req_status_code_ == 500:
            self.__g_logger_info.error('dingtalkApiError: 本地中间件Api服务异常. apiname: {a}. errcode: {c}. errmsg: {e}'.format(a=req_api_name_, c=req_status_code_, e=str(req_result_)))
        elif req_status_code_ != 200:
            self.__g_logger_info.error('dingtalkApiError. apiname: {a}. errcode: {c}. errmsg: {e}'.format(a=req_api_name_, c=req_status_code_, e=str(req_result_)))
        else:
            return True


class APITools:
    '''
    辅助工具类
    '''

    @staticmethod
    def custom_random(input_, n_, flag_):
        """
        自定义取小数点后n位, flag的 0: 四舍五入, 1: 向下取整, 2: 向上取整
        """

        # custom_random = lambda r,n: str(r)[:str(r).rfind('.') + n + 1]
        num = str(input_)
        mash = num[num.rfind('.') + 1 :]
        if flag_ == 0:
            for nx in range(len(mash)):
                if n_ == 0:
                    if mash[0] <= 4:
                        return num[: num.find('.')]
                    else:
                        return num[: num.find('.')] + 1
                else:
                    if nx <= n_ + 1:
                        if mash[nx] < 4:
                            return num[: num.find('.') + n_]
                        elif mash[nx] == 4:
                            continue
                        else:
                            # n=0 : +1
                            # n=1 : +0.1
                            # n=2 : +0.01
                            # ...
                            return num[: num.find('.') + n_ + 1] + (1 / 10**n_)
                    else:
                        print('#')
        elif flag_ == 1:
            return num[: num.find('.') + n_ + 1]
        elif flag_ == 2:
            return num[: num.find('.') + n_ + 1] + (1 / 10**n_)
        else:
            return "flag为错误值"

    @staticmethod
    def WriteJson(json_: object, filedir_: str, filename_: str, prefix_: str = 'OpenAPI_', flag_: int = -1):
        """
        输出json数据到文件
        json_       : 写入的json
        filedir_    : 写入的文件夹路径
        filename_   : 写入的文件名称
        flag_       : print输出执行结果
        """
        writeJson = {'writeTime': time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())), 'result': json_}
        with open(os.path.join(filedir_, f"{prefix_}{filename_}.json"), 'w', encoding='utf-8') as f:
            f.write(json.dumps(writeJson, indent=2, ensure_ascii=False))
        print(f"执行写入:{filedir_}\\{prefix_}{filename_}.json") if flag_ == -1 else ''

    @staticmethod
    def loop_dir(fullname_: str, num: int = 1):
        '''
        新建指定名称的文件夹
        xxxx-xx-xx xx.NODE.1
        xxxx-xx-xx xx.NODE.2
        xxxx-xx-xx xx.NODE....
        '''
        programFullPath = fullname_[: fullname_.rfind('.') + 1] + str(num)

        if os.path.exists(programFullPath):
            num += 1
            return APITools.loop_dir(fullname_=programFullPath, num=num)
        else:
            return programFullPath
