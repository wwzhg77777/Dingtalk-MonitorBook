#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-09-19
@FilePath    :  callback_0001.py
@FileVersion :  1.0
@LastEditTime:  2023-09-19
@FileDesc    :  API接口: 钉钉通讯录变更告警-callback_0001
'''

import os
import time
import json

from requests import post

from components.DingtalkOpenAPI import DingtalkOpenAPI
from components.LocalOpenAPI import LocalOpenAPI
from components.MySQLHandle import MySQLHandle
from utils.utils_config import DD_CONFIG_GLOBAL, DD_CONFIG_CALLBACK_0001
from utils.utils_const import CONST
from utils.utils_func import unix2formatTime
from utils.utils_mysqli import get_insert_sql
from dingtalkchatbot.chatbot import DingtalkChatbot


def sync_mysql(data: dict):
    sql_handle = MySQLHandle()
    sql_handle.connect()
    insert_sql = get_insert_sql(
        'monitor_book_logs',
        False,
        {
            'id': int(time.mktime(time.strptime(data['time'], '%Y-%m-%d %H:%M:%S'))),
            'type': data['eventtype'] if data.__contains__('eventtype') else '',
            'title': data['eventtitle'] if data.__contains__('eventtitle') else '',
            'time': data['time'],
            'item': json.dumps(data['item'], ensure_ascii=False) if data.__contains__('item') else '',
            'data': json.dumps(data['data'], ensure_ascii=False) if data.__contains__('data') else '',
        },
    )
    sql_handle.execute(insert_sql)
    sql_handle.close_conn()


def callback_0001(rootpath_: str, dd_msg: str, kwargs):
    '''
        API接口: 钉钉通讯录变更告警-callback_0001
        rootpath_   : 当前项目的根目录
        dd_msg      : 钉钉回调数据
        kwargs      : 不定参数集

    SUCCESS
    return None     : 默认返回 None

    ERROR
    return False    : 错误返回 False
    '''

    dingApi: DingtalkOpenAPI = kwargs['ding_api']
    localApi: LocalOpenAPI = kwargs['local_api']
    robot: DingtalkChatbot = kwargs['robot']

    write_json_item = {'eventtype': '', 'eventtitle': '', 'time': '', 'item': {}, 'data': []}

    with open(os.path.join(rootpath_, 'src', 'temp', f"{dd_msg['TimeStamp']}_{dd_msg['EventType']}"), 'a', encoding='utf-8') as f:
        callback_msg = ''
        callback_msg_title = ''
        f.write(f"[{unix2formatTime(int(time.time()))}]\t\t")  # 缓存result信息到temp目录

        if dd_msg['EventType'] == 'user_add_org':
            callback_msg_title = '企业增加员工'
            callback_msg += f"#### <font color=\"#0000FF\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**操作时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "

            write_json_item['eventtype'] = 'user_add_org'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)

            for newUserId in dd_msg['UserId']:
                newUserItem = dingApi.get_userInfo(userid=newUserId)
                callback_msg += f"**新增用户：<font color=\"#0000FF\">{newUserItem[0]['result']['name'] if newUserItem != None and newUserItem[0]['errcode'] == 0 else ''}</font>"
                callback_msg += f"({newUserId})**  \n\n  "
                f.write(f"get new UserId:{newUserId}" + f", UserName:{newUserItem[0]['result']['name'] if newUserItem != None and newUserItem[0]['errcode'] == 0 else ''}\r\n")
                write_json_item['data'].append({'id': newUserId, 'name': newUserItem[0]['result']['name'] if newUserItem != None and newUserItem[0]['errcode'] == 0 else ''})

        elif dd_msg['EventType'] == 'user_modify_org':
            callback_msg_title = '员工信息修改'
            if len(dd_msg['diffInfo']) > 1:
                f.write('current is error, diffInfo len is more.')
                return
            elif not dd_msg.__contains__('OptStaffId'):
                f.writelines('OptStaffId is null.\r\n')

            optStaffItem = dingApi.get_userInfo(userid=dd_msg['OptStaffId']) if dd_msg.__contains__('OptStaffId') else None
            callback_msg += f"#### <font color=\"#0000FF\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**修改时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "
            callback_msg += f"**操作人：{optStaffItem[0]['result']['name'] if optStaffItem != None and optStaffItem[0]['errcode'] == 0 else ''}"
            callback_msg += f"({dd_msg['OptStaffId'] if dd_msg.__contains__('OptStaffId') else None})**  \n\n  "
            callback_msg += f"**修改用户：{dd_msg['diffInfo'][0]['curr']['name']}({dd_msg['diffInfo'][0]['userid']})**  \n\n  "

            write_json_item['eventtype'] = 'user_modify_org'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)
            write_json_item['item']['optstaffid'] = dd_msg['OptStaffId'] if dd_msg.__contains__('OptStaffId') else None
            write_json_item['item']['optstaffname'] = optStaffItem[0]['result']['name'] if optStaffItem != None and optStaffItem[0]['errcode'] == 0 else ''
            write_json_item['item']['userid'] = dd_msg['diffInfo'][0]['userid']
            write_json_item['item']['username'] = dd_msg['diffInfo'][0]['curr']['name']

            prev_userinfo: dict = dd_msg['diffInfo'][0]['prev']
            curr_userinfo: dict = dd_msg['diffInfo'][0]['curr']
            is_prev_more: bool = len(prev_userinfo) > len(curr_userinfo)  # 修改前的字段数量 大于 修改后的字段数量
            moreFieldItem = prev_userinfo if is_prev_more else curr_userinfo
            for k in moreFieldItem.keys():
                prev_value = prev_userinfo[k] if k in prev_userinfo.keys() else ''
                curr_value = curr_userinfo[k] if k in curr_userinfo.keys() else ''
                try:
                    tmp_prev = json.loads(prev_value, strict=False)
                    prev_value = tmp_prev
                except json.decoder.JSONDecodeError:
                    pass
                try:
                    tmp_curr = json.loads(curr_value, strict=False)
                    curr_value = tmp_curr
                except json.decoder.JSONDecodeError:
                    pass
                if k in DD_CONFIG_CALLBACK_0001.user_modify_field_maps.keys():
                    if DD_CONFIG_CALLBACK_0001.user_modify_field_maps[k] == '直属主管' and prev_value != curr_value:
                        prev_userItem = dingApi.get_userInfo(userid=prev_value)
                        prev_userValue = prev_userItem[0]['result']['name'] if prev_userItem != None and prev_userItem[0]['errcode'] == 0 else ''
                        curr_userItem = dingApi.get_userInfo(userid=curr_value if prev_value == '' else prev_value)
                        curr_userValue = curr_userItem[0]['result']['name'] if curr_userItem != None and curr_userItem[0]['errcode'] == 0 else ''
                        callback_msg += f"**修改字段：<font color=\"#FF0000\">{DD_CONFIG_CALLBACK_0001.user_modify_field_maps[k]}</font>**  \n\n  "
                        callback_msg += f"- 修改前：{prev_userValue}({prev_value})  \n\n  - 修改后：{curr_userValue}({curr_value})  \n\n  "
                        write_json_item['data'].append({'field': DD_CONFIG_CALLBACK_0001.user_modify_field_maps[k], 'prev_value': f"{prev_userValue}({prev_value})", 'curr_value': f"{curr_userValue}({curr_value})"})
                    elif prev_value != curr_value:
                        callback_msg += f"**修改字段：<font color=\"#FF0000\">{DD_CONFIG_CALLBACK_0001.user_modify_field_maps[k]}</font>**  \n\n  - 修改前：{prev_value}  \n\n  - 修改后：{curr_value}  \n\n  "
                        write_json_item['data'].append({'field': DD_CONFIG_CALLBACK_0001.user_modify_field_maps[k], 'prev_value': prev_value, 'curr_value': curr_value})

            f.write(
                f"get change OptStaffId:{dd_msg['OptStaffId'] if dd_msg.__contains__('OptStaffId') else None}"
                + f", OptStaffName:{optStaffItem[0]['result']['name'] if optStaffItem != None and optStaffItem[0]['errcode'] == 0 else ''}"
                + f", UserId:{dd_msg['diffInfo'][0]['userid']}"
                + f", UserName:{dd_msg['diffInfo'][0]['curr']['name']}"
            )
            if len(write_json_item['data']) == 0 and not dd_msg.__contains__('OptStaffId'):
                return

        elif dd_msg['EventType'] == 'user_leave_org':
            callback_msg_title = '企业员工离职'
            callback_msg += f"#### <font color=\"#FF0000\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**操作时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "

            write_json_item['eventtype'] = 'user_leave_org'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)

            for leaveUserId in dd_msg['UserId']:
                leaveUserValue = localApi.get_historyUserInfo(userid=leaveUserId)
                callback_msg += f"**离职用户：<font color=\"#0000FF\">{leaveUserValue['name'] if leaveUserValue is not None else ''}</font>"
                callback_msg += f"({leaveUserId})**  \n\n  "
                f.write(f"get leave UserId:{leaveUserId}" + f", UserName:{leaveUserValue['name'] if leaveUserValue is not None else ''}\r\n")
                write_json_item['data'].append({'id': leaveUserId, 'name': leaveUserValue['name'] if leaveUserValue is not None else ''})

        elif dd_msg['EventType'] == 'user_active_org':
            callback_msg_title = '企业激活员工'
            callback_msg += f"#### <font color=\"#0000FF\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**操作时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "

            write_json_item['eventtype'] = 'user_active_org'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)

            for activeUserId in dd_msg['UserId']:
                activeUserItem = dingApi.get_userInfo(userid=activeUserId)
                callback_msg += f"**激活用户：<font color=\"#0000FF\">{activeUserItem[0]['result']['name'] if activeUserItem != None and activeUserItem[0]['errcode'] == 0 else ''}</font>"
                callback_msg += f"({activeUserId})**  \n\n  "
                f.write(f"get active UserId:{activeUserId}" + f", UserName:{activeUserItem[0]['result']['name'] if activeUserItem != None and activeUserItem[0]['errcode'] == 0 else ''}\r\n")
                write_json_item['data'].append({'id': activeUserId, 'name': activeUserItem[0]['result']['name'] if activeUserItem != None and activeUserItem[0]['errcode'] == 0 else ''})

        elif dd_msg['EventType'] == 'org_dept_create':
            callback_msg_title = '企业新增部门'
            callback_msg += f"#### <font color=\"#0000FF\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**操作时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "

            write_json_item['eventtype'] = 'org_dept_create'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)

            for newDeptId in dd_msg['DeptId']:
                parentDeptItems = dingApi.get_listParentByDept(dept_id=newDeptId)
                if parentDeptItems is not None and parentDeptItems[0]['errcode'] == 0:
                    currDeptItem = dingApi.get_deptInfo(dept_id=newDeptId)
                    callback_msg += f"**新增部门：<font color=\"#0000FF\">{currDeptItem[0]['result']['name'] if currDeptItem != None and currDeptItem[0]['errcode'] == 0 else ''}</font>"
                    callback_msg += f"({newDeptId})**  \n\n  "

                    parentDeptNames = []
                    if len(parentDeptItems[0]['result']['parent_id_list']) > 1:
                        for childDeptId in parentDeptItems[0]['result']['parent_id_list']:
                            if childDeptId == parentDeptItems[0]['result']['parent_id_list'][0]:
                                childDeptItem = currDeptItem
                            else:
                                childDeptItem = dingApi.get_deptInfo(dept_id=childDeptId)
                            parentDeptNames.append(childDeptItem[0]['result']['name'] if childDeptItem != None and childDeptItem[0]['errcode'] == 0 else '')
                        callback_msg += f"**部门完整名称：{'/'.join(parentDeptNames[::-1])}**  \n\n  "
                f.write(f"get new CurrDeptId:{newDeptId}" + f", CurrDeptName:{currDeptItem[0]['result']['name'] if currDeptItem != None and currDeptItem[0]['errcode'] == 0 else ''}\r\n")
                f.write(f"get new FullDeptName:{'/'.join(parentDeptNames[::-1])}\r\n\r\n")
                write_json_item['data'].append({'id': newDeptId, 'name': currDeptItem[0]['result']['name'] if currDeptItem != None and currDeptItem[0]['errcode'] == 0 else '', 'fullname': '/'.join(parentDeptNames[::-1])})

        elif dd_msg['EventType'] == 'org_dept_modify':
            callback_msg_title = '企业修改部门'
            callback_msg += f"#### <font color=\"#0000FF\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**操作时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "

            write_json_item['eventtype'] = 'org_dept_modify'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)

            for modDeptId in dd_msg['DeptId']:
                parentDeptItems = dingApi.get_listParentByDept(dept_id=modDeptId)
                if parentDeptItems is not None and parentDeptItems[0]['errcode'] == 0:
                    currDeptItem = dingApi.get_deptInfo(dept_id=modDeptId)
                    callback_msg += f"**修改部门：<font color=\"#0000FF\">{currDeptItem[0]['result']['name'] if currDeptItem != None and currDeptItem[0]['errcode'] == 0 else ''}</font>"
                    callback_msg += f"({modDeptId})**  \n\n  "

                    parentDeptNames = []
                    if len(parentDeptItems[0]['result']['parent_id_list']) > 1:
                        for childDeptId in parentDeptItems[0]['result']['parent_id_list']:
                            if childDeptId == parentDeptItems[0]['result']['parent_id_list'][0]:
                                childDeptItem = currDeptItem
                            else:
                                childDeptItem = dingApi.get_deptInfo(dept_id=childDeptId)
                            parentDeptNames.append(childDeptItem[0]['result']['name'] if childDeptItem != None and childDeptItem[0]['errcode'] == 0 else '')
                        callback_msg += f"**部门完整名称：{'/'.join(parentDeptNames[::-1])}**  \n\n  "
                f.write(f"get modify CurrDeptId:{modDeptId}" + f", CurrDeptName:{currDeptItem[0]['result']['name'] if currDeptItem != None and currDeptItem[0]['errcode'] == 0 else ''}\r\n")
                f.write(f"get modify FullDeptName:{'/'.join(parentDeptNames[::-1])}\r\n\r\n")
                write_json_item['data'].append({'id': modDeptId, 'name': currDeptItem[0]['result']['name'] if currDeptItem != None and currDeptItem[0]['errcode'] == 0 else '', 'fullname': '/'.join(parentDeptNames[::-1])})

        elif dd_msg['EventType'] == 'org_dept_remove':
            callback_msg_title = '企业删除部门'
            callback_msg += f"#### <font color=\"#FF0000\">**{callback_msg_title}**</font>  \n\n  "
            callback_msg += f"**操作时间：{unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)}**  \n\n  "

            write_json_item['eventtype'] = 'org_dept_remove'
            write_json_item['eventtitle'] = callback_msg_title
            write_json_item['time'] = unix2formatTime(_unix=dd_msg['TimeStamp'], _isUnit10=False)

            for delDeptId in dd_msg['DeptId']:
                delDeptValue = localApi.get_historyDeptInfo(deptid=delDeptId)
                callback_msg += f"**删除部门：<font color=\"#0000FF\">{delDeptValue['name'] if delDeptValue is not None else ''}</font>"
                callback_msg += f"({delDeptId})**  \n\n  "
                callback_msg += f"**部门完整名称：{delDeptValue['fullname'] if delDeptValue is not None else ''}**  \n\n  "
                f.write(f"get delete DeptId:{delDeptId}" + f", DeptName:{delDeptValue['name'] if delDeptValue is not None else ''}\r\n")
                f.write(f"get delete FullDeptName:{delDeptValue['fullname'] if delDeptValue is not None else ''}")
                write_json_item['data'].append({'id': delDeptId, 'name': delDeptValue['name'] if delDeptValue is not None else '', 'fullname': delDeptValue['fullname'] if delDeptValue is not None else ''})
    robot.send_markdown(title=callback_msg_title, text=callback_msg, is_at_all=False) if DD_CONFIG_GLOBAL.webhook_info_flag else ''  # webhook发送给钉钉群聊
    sync_mysql(write_json_item)
