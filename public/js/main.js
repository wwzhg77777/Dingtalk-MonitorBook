/*
 * @Author      :  ww1372247148@163.com
 * @AuthorDNS   :  wendirong.top
 * @CreateTime  :  2024-01-05
 * @FilePath    :  main.js
 * @FileVersion :  1.0
 * @FileDesc    :  全局通用的js函数集
*/

var monitorbook_table_cols = [
    [
        {
            field: 'eventtype',
            title: '事件分类',
            width: 120,
            align: 'center',
            sort: true,
            templet: '#monitorbook-tpl-eventtype',
        }, {
            field: 'eventtitle',
            title: '事件标题',
            width: 160,
            align: 'center',
            sort: true,
            templet: '#monitorbook-tpl-eventtitle',
        }, {
            field: 'time',
            title: '时间',
            width: 200,
            align: 'center',
            sort: true,
            templet: '#monitorbook-tpl-time',
        }, {
            field: 'data',
            title: '日志1',
            minWidth: 800,
            align: 'center',
            templet: '#monitorbook-tpl-data',
        }, {
            field: 'item',
            title: '日志2',
            minWidth: 400,
            align: 'center',
            templet: '#monitorbook-tpl-item',
        }
    ]
];