-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- 主机： nginx.mysite.com
-- 生成日期： 2024-01-29
-- 服务器版本： 8.0.24
-- PHP 版本： 7.4.30(cli)
SET
  SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

SET
  time_zone = "+00:00";

--
-- 数据库： `monitor_book`
--
-- CREATE DATABASE `monitor_book`;
use `monitor_book`;


CREATE TABLE `monitor_book_logs` (
  `id` CHAR(40) NOT NULL PRIMARY KEY COMMENT 'ID',
  `type` VARCHAR(200) NOT NULL COMMENT '事件分类',
  `title` VARCHAR(200) NULL COMMENT '事件标题',
  `time` VARCHAR(50) NULL COMMENT '时间',
  `data` TEXT NULL COMMENT '日志1',
  `item` TEXT NULL COMMENT '日志2',
  `CreateTime` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) COMMENT '钉钉通讯录变更告警的日志表';
