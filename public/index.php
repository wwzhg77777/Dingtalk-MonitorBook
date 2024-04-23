<?php
#
# @Author      :  ww1372247148@163.com
# @AuthorDNS   :  wendirong.top
# @CreateTime  :  2024-01-05
# @FilePath    :  index.php
# @FileVersion :  1.2
# @LastEditTime:  2024-01-05
# @FileDesc    :  index页面.
#

if (isset($_REQUEST['type']) && $_REQUEST['type'] == 'search') {
    $require_target = true;
    if (isset($_REQUEST['stime']) && isset($_REQUEST['etime'])) {
        $stime = $_REQUEST['stime'];
        $etime = $_REQUEST['etime'];
    }
    if (isset($_REQUEST['time'])) {
        header('Location: /?type=search&getall=true&stime=&etime=');
    }
}
?>
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="description" content="钉钉通讯录变更数据展示">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="maximum-scale=1.0,minimum-scale=1.0,user-scalable=0,width=device-width,initial-scale=1.0" />
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta name="format-detection" content="telephone=no,email=no,adress=no" />
    <meta content="no" name="apple-mobile-web-app-capable" />
    <meta content="black" name="apple-mobile-web-app-status-bar-style" />
    <title>钉钉通讯录变更数据展示</title>
    <link rel="stylesheet" href="./layui/css/layui.css">
    <link rel="stylesheet" href="./css/index.css">
    <link rel="stylesheet" href="./css/index_media.css">
    <!-- 移动端调试 -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/eruda"></script>
    <script>
        eruda.init();
    </script> -->
    <!-- 移动端调试  -->
</head>

<body>
    <div class="layui-layout layui-layout-admin">
        <?php require_once 'template/header.php'; // 填充header页头
        if (isset($require_target)) { ?>
            <div class="layui-body">
                <!-- 内容主体区域 -->
                <table id="monitorbook_t_main" lay-filter="tableEvent"></table>

                <script type="text/html" id="monitorbook_t_main_toolbar">
                    <div class="monitorbook-cls-toolbar-left">
                        <div class="layui-form">
                            <button class="layui-btn layui-btn-sm tool-temp-button" lay-event="getall">查看全部数据</button>
                        </div>
                    </div>
                    <div class="monitorbook-cls-toolbar-right">
                        <button class="layui-btn layui-btn-sm tool-temp-button tool-opacity" lay-event="LAYTABLE_COLS">筛选列</button>
                        <button class="layui-btn layui-btn-sm tool-temp-button tool-opacity" lay-event="exportFile">导出</button>
                    </div>
                </script>
            </div>
        <?php } else {
            echo "<div class=\"layui-body\">\r\n\t";
            echo "<h1 style=\"margin-top:80px;margin-left:120px;\">当前查询内容为空。</h1>\r\n\t";
            echo '</div>';
        }
        require_once 'template/footer.php'; // 填充footer页尾
        ?>
    </div>

    <script src="./layui/layui.js"></script>
    <script src="./js/main.js"></script>
    <script src="./js/utils.js"></script>
    <script src="./js/index.js"></script>
    <script src="./js/jquery.min.js"></script>
    <script src="./js/jquery.base64.js"></script>
    <script src="./js/crypto-js.min.js"></script>
    <script>
        localStorage.clear();
        sessionStorage.clear();

        const API_URI_SCHEME_HOST = 'https://api.monitor-book.mysite.com';

        // layui 模块化table [ 2024.1 by wendr ]
        layui.use(['table', 'layer', 'laypage', 'laytpl', 'jquery'], () => {
            let table = layui.table,
                layer = layui.layer,
                laypage = layui.laypage,
                laytpl = layui.laytpl,
                $ = layui.jquery;

            table.render({
                elem: '#monitorbook_t_main',
                title: '钉钉通讯录变更数据展示',
                height: 'full-60',
                toolbar: '#monitorbook_t_main_toolbar',
                defaultToolbar: [],
                url: API_URI_SCHEME_HOST + '/getData',
                method: 'get',
                where: {
                    token: CryptoJS.MD5('get_data').toString(),
                    mode: 'get_data',
                    getall: <?= $_REQUEST['getall']; ?>,
                    stime: '<?= $stime; ?>',
                    etime: '<?= $etime; ?>'
                },
                page: {
                    groups: 10
                },
                limit: 300,
                limits: [300, 500, 1000, 3000, 10000],
                size: 'lg',
                escape: true,
                cols: monitorbook_table_cols,
                parseData: (res) => {
                    return {
                        'code': res.code,
                        'msg': res.msg,
                        'count': res.count,
                        'data': res.data,
                    };
                },
                done: (res, curr, count) => {
                    // layui 统计临时数据 [ 2023.12 by wendr ]
                    baseData = deepClone(res.data);

                    // laypage组件添加 当前选择n行 [ 2023.3 by wendr ]
                    var checkStatus = table.checkStatus('monitorbook_t_main');
                    let doSelectDom = document.createElement('span');
                    doSelectDom.id = 'selectRows';
                    doSelectDom.innerText = '当前已选择 ' + checkStatus['data'].length + ' 行';
                    $('.layui-box.layui-laypage.layui-laypage-default').append(doSelectDom);
                }
            });

            // 表格工具栏事件 [ 2024.1 by wendr ]
            table.on('toolbar(tableEvent)', (obj) => {
                switch (obj.event) {
                    case 'exportFile':
                        if (baseData.length > 0) {
                            table.exportFile(obj.config.id, baseData, 'xls');
                        } else {
                            if (typeof obj.config.data !== 'undefined' && obj.config.data.length > 0) {
                                table.exportFile(obj.config.id, obj.config.data, 'xls');
                            }
                        }
                        break;
                    case 'getall':
                        getall();
                        break;
                }
            });
        });
    </script>
    <!-- layui_templet 模板引擎 [ 2024.1 by wendr ] -->
    <?php
    if (isset($require_target)) {
        require_once "components/templet.php";    // 填充component模块对应的layui_templet模板引擎
    }
    ?>
</body>

</html>