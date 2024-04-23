#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-09-19
@FilePath    :  utils_config.py
@FileVersion :  1.0
@LastEditTime:  2023-09-19
@FileDesc    :  记录不同参数的配置信息
'''


class DD_CONFIG_GLOBAL:
    '''
    对接钉钉内部应用的全局配置信息
    '''

    subscribe_events = ['user_add_org', 'user_modify_org', 'user_leave_org', 'user_active_org', 'org_dept_create', 'org_dept_modify', 'org_dept_remove', 'label_user_change', 'label_conf_add', 'label_conf_del']
    '''允许接收的钉钉回调事件类型名称'''

    debug_print_flag = -1
    '''-1: 不打印     0: 打印特定内容      1: 打印url参数+解密后原文   2: 打印request参数+url参数+解密后原文'''

    webhook_error_flag = True
    '''error信息是否发送webhook. False: 不发送webhook     True: 发送webhook'''

    webhook_info_flag = False
    '''info信息是否发送webhook. False: 不发送webhook     True: 发送webhook'''


class DD_CONFIG_CALLBACK_0001:
    '''
    钉钉通讯录变更告警-callback_0001的配置信息
    '''

    groupChat_robot_webhook_secret: str = 'your_webhook_secret'
    '''钉钉群聊机器人的Webhook密钥'''
    groupChat_robot_webhook_link: str = 'your_webhook_link'
    '''钉钉群聊机器人的Webhook访问链接'''

    user_modify_field_maps = {
        'work_place': '办公地点',
        'manager_userid': '直属主管',
        'name': '姓名',
        'telephone': '分机号',
        'remark': '备注',
        'job_number': '工号',
        'hired_date': '入职时间',
        'email': '企业邮箱',
        'ext_fields': '扩展字段',
    }
