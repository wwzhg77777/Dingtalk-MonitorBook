<?php
#
# @Author      : ww1372247148@163.com
# @AuthorDNS   : wendirong.top
# @CreateTime  : 2024-01-08
# @FilePath    : components/templet.php
# @FileVersion : 1.0
# @FileDesc    : compontents的 layui_templet模板引擎
#
?>

<script type="text/html" id="monitorbook-tpl-eventtype">
{{# if (d.eventtype.startsWith('user_')){ }}
    <p>员工</p>
    {{# } else if (d.eventtype.startsWith('org_dept_')){ }}
        <p>部门</p>
        {{# } }}
</script>
<script type="text/html" id="monitorbook-tpl-eventtitle">
{{# if(d.eventtype == 'user_leave_org' || d.eventtype == 'org_dept_remove'){ }}
    <p style="color: #FF0000;">{{ d.eventtitle }}</p>
    {{# } else { }}
        <p style="color: #0000FF;">{{ d.eventtitle }}</p>
        {{# } }}
</script>
<script type="text/html" id="monitorbook-tpl-time">
{{ d.time }}
</script>
<script type="text/html" id="monitorbook-tpl-data">
{{# if (d.data.length > 0){ }}
    {{# for (let i = 0; i < d.data.length; i++){ }}
        <div style="display: flex; padding: 3px 0;">
            {{# if (Object.keys(d.item).length > 0){ }}
                <span class="cls-data-field cls-overhidden">修改字段：<font color="#FF0000">{{ d.data[i].field }}</font></span>
                <span class="cls-data-value cls-overhidden" title={{ JSON.stringify(d.data[i].prev_value) }}>修改前：{{ JSON.stringify(d.data[i].prev_value).slice(1,-1) }}</span>
                <span class="cls-data-value cls-overhidden" title={{ JSON.stringify(d.data[i].curr_value) }}>修改后：{{ JSON.stringify(d.data[i].curr_value).slice(1,-1) }}</span>
                {{# } else if (d.eventtype.startsWith('org_dept_')){ }}
                    <span>
                        <p>部门：<font color="#0000FF">{{ d.data[i].name }}</font>({{ d.data[i].id }})</p>
                        <p>部门完整名称：{{ d.data[i].fullname }}</p>
                    </span>
                    {{# } else { }}
                        <p>用户：<font color="#0000FF">{{ d.data[i].name }}</font>({{ d.data[i].id }})</p>
                        {{# } }}

        </div>
        {{# } }}
            {{# } }}
</script>
<script type="text/html" id="monitorbook-tpl-item">
{{# if (Object.keys(d.item).length > 0){ }}
    <span>
        <p>操作人：{{ d.item.optstaffname }}({{ d.item.optstaffid }})</p>
        <p>修改用户：{{ d.item.username }}({{ d.item.userid }})</p>
    </span>
    {{# } }}
</script>