#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author      :  ww1372247148@163.com
@AuthorDNS   :  wendirong.top
@CreateTime  :  2024-01-29
@FilePath    :  MySQLHandle.py
@FileVersion :  1.0
@LastEditTime:  2024-01-29
@FileDesc    :  用于读写MySQL数据库的MySQL操作类
'''

from pymysql import err
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from . import *


class MySQLHandle:
    '''
    用于读写MySQL数据库的MySQL操作类
    '''

    _host: str = None
    _port: int = None
    _user: str = None
    _pass: str = None
    _database: str = None
    _charset: str = 'utf8mb4'

    _sql_conn: Connection = None
    _cursor: Cursor = None
    _sql_error = None

    def __init__(self, host_: str = 'localhost', port_: int = 3306, user_: str = 'monitor_book', pass_: str = 'you_mysql_pass', database_: str = 'monitor_book'):
        '''
        host_       : MySQL 服务器完全限定域名
        port_       : MySQL 端口
        user_       : MySQL 用户
        pass_       : MySQL 密码
        database_   : MySQL 数据库
        '''
        self._host = host_
        self._port = port_
        self._user = user_
        self._pass = pass_
        self._database = database_

    def connect(self, is_autocommit_: bool = False):
        '''
            连接到MySQL数据库
            is_autocommit_  : 是否启用自动提交sql语句

        SUCCESS
        return True     : 成功返回 True

        ERROR
        return False    : 错误返回 False
        '''
        if self._sql_error is None:
            try:
                if self._sql_conn and not self._cursor:
                    self._cursor = self._sql_conn.cursor()
                    return True
                elif self._sql_conn and self._cursor:
                    return True
                else:
                    self._sql_conn = Connection(host=self._host, port=self._port, user=self._user, password=self._pass, database=self._database, charset=self._charset, autocommit=is_autocommit_)
                    if self._sql_conn:
                        self._cursor = self._sql_conn.cursor()
                        return True
                    else:
                        return False
            except err.MySQLError as e:
                return self.return_error_conn(e)
        else:
            return False

    def get_cursor(self):
        '''
            返回已连接MySQL数据库的cursor游标对象

        SUCCESS
        return cursor   : 成功返回 cursor游标对象

        ERROR
        return None     : 错误返回 None
        '''
        if self._cursor:
            return self._cursor
        else:
            return None

    def execute(self, sql_: str, is_commit_: bool = True):
        '''
            MySQL数据库执行sql语句并返回结果集或结果

        SUCCESS
        return dict | True    : select查询成功返回 dict对象, json格式. other执行成功返回 True

        ERROR
        return None | False   : select查询错误返回 None. other执行错误返回 False
        '''
        if self._sql_error is None:
            try:
                if 'SELECT' in sql_.upper():
                    self._cursor.execute(sql_)
                    ret_set = self._cursor.fetchall()
                    return ret_set
                elif 'UPDATE' in sql_.upper() or 'TRUNCATE TABLE' in sql_.upper():
                    self._cursor.execute(sql_)
                    self._sql_conn.commit() if is_commit_ else ''
                    return True
                else:
                    if self._cursor.execute(sql_) == 1:
                        self._sql_conn.commit() if is_commit_ else ''
                        return True
                    else:
                        return False
            except err.MySQLError as e:
                return self.return_error_execute(e)
        else:
            return False

    def return_error_conn(self, err_: str):
        '''
        统一处理MySQL的错误返回信息, 错误域: Connection
        err_    : 错误信息的源文本
        '''
        if type(err_.args) == tuple:
            if err_.args[0] == 2003:
                err_code = err_.args[0]
                err_msg = 'MySQL 连接被拒绝, host或port的配置错误'
            elif err_.args[0] == 1044:
                err_code = err_.args[0]
                err_msg = 'MySQL 连接数据库失败, 数据库不存在|无权限|配置错误'
            elif err_.args[0] == 1045:
                err_code = err_.args[0]
                err_msg = 'MySQL 用户登录失败, 用户不存在|密码错误'
        else:
            err_code = 500
            err_msg = '500错误'

        if type(err_.args) == tuple:
            self._sql_error = (err_code, str(err_.args[1]), err_msg)
        else:
            self._sql_error = (err_code, str(err_.args), err_msg)
        self.close_conn()
        return False

    def return_error_execute(self, err_: str):
        '''
        统一处理MySQL的错误返回信息, 错误域: insert | delete | update | select
        err_    : 错误信息的源文本
        '''
        self._sql_conn.rollback()
        self._ldap_error = (400, str(err_), 'MySQL execute error')
        return None

    def close_conn(self):
        '''
        关闭MySQL连接
        '''
        if self._sql_conn:
            if self._sql_conn.open:
                self._sql_conn.close()
            del self._sql_conn
        if self._cursor:
            del self._cursor
