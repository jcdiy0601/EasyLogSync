$(function () {
    $("#update_btn").click(function () {
        // 清空结果栏
        $("#task_result_container").empty();
        // 获取select值
        var appValue = $("#app-select").val();
        // 显示等待图标
        var load_li = '<li><pre><i class="fa fa-spinner fa-spin" aria-hidden="true"></i></pre></li>';
        $("#task_result_container").append(load_li);
        // 发送ajax到后台
        $.ajax({
            url: "update_log.html",
            type: "POST",
            dataType: "JSON",
            headers: {"X-CSRFtoken": $.cookie("csrftoken")},
            data: {"app_value": appValue},
            success: function (response) {
                if (response.status) {
                    $("#task_result_container").empty();
                    var res_li = "<li><pre>" + response.message + "</pre></li>";
                    $("#task_result_container").append(res_li);
                } else {
                    $("#task_result_container").empty();
                    var err_li = "<li><pre>" + response.message + "<br/>" + response.error + "</pre></li>";
                    $("#task_result_container").append(err_li);
                }
            },
            error: function () {

            }
        });
    });

});