(function (jq) {
    // 初始化表格的头部
    function initTableHeader() {
        var $header = $("#log_table thead");
        $header.empty();
        var theadTr = "<tr><td>日志名称</td><td>时间</td><td>大小</td><td>操作</td></tr>";
        $header.append(theadTr);
    }

    // 初始化表格的内容
    function initTableBody(dataList) {
        var $body = $("#log_table tbody");
        // 清空body中的内容
        $body.empty();
        $.each(dataList, function (k1, file_info) {
            var tr = document.createElement("tr");
            var logNameTd = document.createElement("td");
            $(logNameTd).text(file_info.file_name);
            $(tr).append(logNameTd);
            var logTimeTd = document.createElement("td");
            $(logTimeTd).text(file_info.file_time);
            $(tr).append(logTimeTd);
            var logSizeTd = document.createElement("td");
            $(logSizeTd).text(file_info.file_size + " MB");
            $(tr).append(logSizeTd);
            var logDownloadTd = document.createElement("td");
            var downloadForm = "<form method='POST' action='download_log.html'><input style='display: none' type='text' name='download_file_path' value='" + file_info.file_path + "'/>" +
                '<button type="submit" class="btn btn-xs btn-default btn-icon icon-lg fa fa-download"></button>' + "</form>";
            $(logDownloadTd).append(downloadForm);
            $(tr).append(logDownloadTd);
            $body.append(tr);
        });

    }

    // 初始化分页内容
    function initPager(pageStr) {
        var $pager = $("#pager");
        $pager.empty();
        $pager.append(pageStr);
    }

    // 绑定点击确定按钮
    $("#choice_btn").click(function () {
        initialize(1);
    });

    // 页面初始化（获取数据，绑定事件）
    function initialize(pager) {
        var $taskResultContainer = $("#task_result_container");
        // 清空结果栏
        $taskResultContainer.empty();
        // 获取select值
        var choiceValue = $("#app-select").val();
        // 显示等待图标
        var load_tag = '<pre><i class="fa fa-spinner fa-spin" aria-hidden="true"></i></pre>';
        $taskResultContainer.append(load_tag);
        // 发送ajax到后台
        $.ajax({
            url: "show_download_log_list.html",
            type: "GET",
            dataType: "JSON",
            data: {"choiceValue": choiceValue, "pager": pager},
            success: function (response) {
                if (response.status) {
                    // 隐藏等待图标
                    $taskResultContainer.empty();
                    // 初始化表标题
                    initTableHeader();
                    // 初始化表内容
                    initTableBody(response.data.data_list);
                    // 初始化页码
                    initPager(response.data.page_info.page_str);
                } else {
                    $taskResultContainer.empty();
                    var err_tag = "<pre>" + response.message + "<br/>" + response.error + "</pre>";
                    $taskResultContainer.append(err_tag);
                }
            },
            error: function () {

            }
        });
    }

    jq.extend({
        // 分页
        "changePage": function (pageNum) {
            initialize(pageNum);
        }
    });
})(jQuery);