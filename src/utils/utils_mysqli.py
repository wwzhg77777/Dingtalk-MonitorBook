#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2023-05-03 17:29:09
@FilePath    :  utils_mysqli.py
@FileVersion :  1.0
@LastEditTime:  2023-05-03 17:29:09
@FileDesc    :  提供python-mysqli工具类函数
'''


def get_insert_sql(tableName_: str, insert_all: bool, *args, **kwargs):
    '''
        构建并返回MySQL的 INSERT 语句. 指定参数args(dict) | 不指定参数args(list)
        tableName_  : table表名称
        insert_all  : True: 不指定写入参数, False: 指定写入参数
        *args       : 不定参数集. list列表允许输入多个参数
        **kwargs    : 不定参数集. dict集合允许输入多个键值对

    SUCCESS
    return str      : 成功返回 str对象: sql语句

    ERROR
    return None     : 错误返回 None
    '''
    # INSERT INTO `table` VALUES ("1", "2", "3", "4", "5")
    if insert_all:
        sql = f"INSERT INTO `{tableName_}` VALUES ("
        for arg in args[0]:
            sql += f"\"{arg}\""
            sql += ', ' if arg != args[0][-1] else ''
        sql += ')'
    # INSERT INTO `table` (`key`, `key1`, `key2`) VALUES ("value", "value1", "value2")
    else:
        sql = f"INSERT INTO `{tableName_}`"
        k_sql = ''
        v_sql = ''
        for arg_k, arg_v in args[0].items():
            k_sql += f"`{arg_k}`"
            v_sql += f"'{arg_v}'"
            if arg_k != list(args[0])[-1]:
                k_sql += ', '
                v_sql += ', '
        sql += f"({k_sql}) VALUES ({v_sql})"
    return sql


def get_delete_sql(tableName_: str, delete_all: bool, *args, **kwargs):
    '''
        构建并返回MySQL的 DELETE 语句. args(dict)为WHERE的keyval
        tableName_  : table表名称
        *args       : 不定参数集. list列表允许输入多个参数
        **kwargs    : 不定参数集. dict集合允许输入多个键值对

    SUCCESS
    return str      : 成功返回 str对象: sql语句

    ERROR
    return None     : 错误返回 None
    '''
    # DELETE FROM `table` WHERE (`key` = "value") AND (`key1` = "value1")
    if delete_all:
        sql = f"TRUNCATE TABLE `{tableName_}`"
    else:
        sql = f"DELETE FROM `{tableName_}` WHERE "
        for arg_k, arg_v in args[0].items():
            sql += f"(`{arg_k}` = \"{arg_v}\")"
            sql += ' AND ' if arg_k != list(args[0])[-1] else ''
    return sql


def get_update_sql(tableName_: str, *args, **kwargs):
    '''
        构建并返回MySQL的 UPDATE 语句. args0(dict)为SET的keyval, args1(dict)为WHERE的keyval
        tableName_  : table表名称
        *args       : 不定参数集. list列表允许输入多个参数
        **kwargs    : 不定参数集. dict集合允许输入多个键值对

    SUCCESS
    return str      : 成功返回 str对象: sql语句

    ERROR
    return None     : 错误返回 None
    '''
    # UPDATE `table` SET `key` = "value", `key1` = "value1" WHERE (`key2` = "value2") AND (`key1` = "value1")
    sql = f"UPDATE `{tableName_}` SET "
    for arg_k, arg_v in args[0].items():
        sql += f"`{arg_k}`={arg_v}" if arg_k in ['ChangeTime', 'ModifyTime', 'OpTime'] and arg_v == 'CURRENT_TIMESTAMP' else f"`{arg_k}`=\"{arg_v}\""
        sql += ', ' if arg_k != list(args[0])[-1] else ''
    sql += ' WHERE '
    for arg_k, arg_v in args[1].items():
        sql += f"(`{arg_k}` = \"{arg_v}\")"
        sql += ' AND ' if arg_k != list(args[1])[-1] else ''
    return sql


def get_select_sql(tableName_: str, select_all: bool, *args, **kwargs):
    '''
        构建并返回MySQL的 SELECT 语句. 指定参数args0(list), args1(dict) | 不指定参数args(dict)
        tableName_  : table表名称
        select_all  : True: 不指定查询参数, False: 指定查询参数
        *args       : 不定参数集. list列表允许输入多个参数
        **kwargs    : 不定参数集. dict集合允许输入多个键值对

    SUCCESS
    return str      : 成功返回 str对象: sql语句

    ERROR
    return None     : 错误返回 None
    '''
    # SELECT * FROM `table` WHERE (`key` = "value") AND (`key1` = "value1")
    if select_all:
        sql = f"SELECT * FROM `{tableName_}` WHERE "
        if len(args) > 0:
            for arg_k, arg_v in args[0].items():
                sql += f"(`{arg_k}` = \"{arg_v}\")"
                sql += ' AND ' if arg_k != list(args[0])[-1] else ''
        else:
            sql += '1'
    # SELECT `key`, `key1`, `key2` FROM `table` WHERE (`key3` = "value3") AND (`key4` = "value4")
    else:
        sql = 'SELECT '
        for arg in args[0]:
            sql += f"`{arg}`"
            sql += ', ' if arg != args[0][-1] else ''
        sql += f" FROM `{tableName_}` WHERE "
        for arg_k, arg_v in args[1].items():
            sql += f"(`{arg_k}` = \"{arg_v}\")"
            sql += ' AND ' if arg_k != list(args[1])[-1] else ''
    return sql
