function initChart() {
    //
    $.ajax({
        url: '/log_web/dashboard_chart1.html',
        type: "GET",
        dataType: "JSON",
        success: function (response) {
            if (response.status) {
                var project_count = parseInt(response.data.project_count);
                var application_count = parseInt(response.data.application_count);
                var user_count = parseInt(response.data.user_count);
                var chart1; // 全局变量
                chart1 = new Highcharts.Chart({
                    chart: {
                        renderTo: 'container-chart1',
                        type: 'column',
                        options3d: {
                            enabled: true,
                            alpha: 10,
                            beta: 25,
                            depth: 75
                        },
                        backgroundColor: null,
                        frame: {
                            bottom: {
                                size: 1,
                                color: 'transparent'
                            },
                            side: {
                                size: 1,
                                color: 'transparent'
                            },
                            back: {
                                size: 1,
                                color: 'transparent'
                            }
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    title: {
                        text: '总览'
                    },
                    subtitle: {
                        text: ''
                    },
                    plotOptions: {
                        column: {
                            depth: 35
                        }
                    },
                    xAxis: {
                        categories: ['类型']
                    },
                    yAxis: {
                        allowDecimals: true,
                        title: {
                            text: '数量'
                        }
                    },
                    series: [
                        {name: '项目', data: [project_count]},
                        {name: '应用', data: [application_count]},
                        {name: '用户', data: [user_count]}
                    ]
                });
            } else {

            }
        },
        error: function () {

        }
    });
}