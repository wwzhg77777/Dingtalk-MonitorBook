# 实时监控钉钉通讯录的变更，通过Webhook发送告警信息到钉钉群聊

 - mysite.com 本地化服务器的主域名
 - nginx.mysite.com 承载web站点的本地化nginx服务器域名
 - monitor-book.mysite.com 挂载在nginx服务器上的web站点及域名
 - api.monitor-book.mysite.com 仅处理web站点的api请求数据接口域名

src\cron目录下使用linux自带的crontab定时任务做执行
js框架使用layui 2.6.8

1. 配置 index.php页面. API_URI_SCHEME_HOST: api接口域名
2. 配置 utils\utils_const.py 的 CONST 变量集
3. 配置 components\MySQLHandle.py 的mysql数据库、用户、密码
