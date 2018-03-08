$(function () {
    // 动态绑定删除按钮
    $("tbody").delegate("button[tag='del-tag']", "click", function () {
        // 获取删除行的uid
        var uid = $(this).attr("uid");
        // 显示模态对话框
        $("#user-del-div").css("display", "block");
        // 点击取消按钮
        $("#cancel-del").click(function () {
            // 关闭模态框
            $("#user-del-div").css("display", "none");
        });
        // 点击关闭按钮
        $("#close-modal-div").click(function () {
            // 关闭模态框
            $("#user-del-div").css("display", "none");
        });
        // 点击确认按钮
        $("#confirm-del").click(function () {
            // 关闭模态框
            $("#user-del-div").css("display", "none");
            // 发送ajax删除数据
            $.ajax({
                url: "user_del.html",
                type: "POST",
                dataType: "JSON",
                headers: {"X-CSRFtoken": $.cookie("csrftoken")},
                data: {"uid": uid},
                success: function (response) {
                    if (response.status) {
                        window.location.reload();
                    } else {
                        $("#user-del-fall").css("display", "block");
                        setTimeout(function () {
                            $("#user-del-fall").css("display", "none");
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