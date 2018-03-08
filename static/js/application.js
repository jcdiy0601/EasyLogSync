$(function () {
    // 动态绑定删除按钮
    $("tbody").delegate("button[tag='del-tag']", "click", function () {
        // 获取删除行的aid
        var aid = $(this).attr("aid");
        // 显示模态对话框
        $("#application-del-div").css("display", "block");
        // 点击取消按钮
        $("#cancel-del").click(function () {
            // 关闭模态框
            $("#application-del-div").css("display", "none");
        });
        // 点击关闭按钮
        $("#close-modal-div").click(function () {
            // 关闭模态框
            $("#application-del-div").css("display", "none");
        });
        // 点击确认按钮
        $("#confirm-del").click(function () {
            // 关闭模态框
            $("#application-del-div").css("display", "none");
            // 发送ajax删除数据
            $.ajax({
                url: "application_del.html",
                type: "POST",
                dataType: "JSON",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                data: {"aid": aid},
                success: function (response) {
                    if (response.status) {
                        window.location.reload();
                    } else {
                        $("#application-del-fall").css("display", "block");
                        setTimeout(function () {
                            $("#application-del-fall").css("display", "none");
                        }, 2000);
                        console.log(response.error);
                    }
                },
                error: function () {

                }
            });
        });
    });
});