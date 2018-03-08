#!/usr/bin/env python
# Author: 'JiaChen'

from django.conf.urls import url
from easy_log_sync_web.views import project_view, application_view, dashboard_view, user_view, log_view

urlpatterns = [
    # 项目管理
    url(r'^project.html$', project_view.project_page, name='project'),
    url(r'^project_add.html$', project_view.project_add, name='project_add'),
    url(r'^project_del.html$', project_view.project_del, name='project_del'),
    url(r'^project_edit_(?P<pid>\d+).html$', project_view.project_edit, name='project_edit'),
    # 应用管理
    url(r'^application.html$', application_view.application_page, name='application'),
    url(r'^application_add.html$', application_view.application_add, name='application_add'),
    url(r'^application_del.html$', application_view.application_del, name='application_del'),
    url(r'^application_edit_(?P<aid>\d+).html$', application_view.application_edit, name='application_edit'),
    # 仪表盘
    url(r'^dashboard_chart1.html', dashboard_view.chart1, name='chart1'),
    # 用户管理
    url(r'^user.html', user_view.user_page, name='user'),
    url(r'^user_add.html$', user_view.user_add, name='user_add'),
    url(r'^user_del.html$', user_view.user_del, name='user_del'),
    url(r'^user_edit_(?P<uid>\d+).html$', user_view.user_edit, name='user_edit'),
    url(r'^user_change_pass_(?P<uid>\d+).html$', user_view.user_change_pass, name='user_change_pass'),
    url(r'^user_relevance_application_(?P<uid>\d+).html$', user_view.user_relevance_application, name='user_relevance_application'),
    # 日志管理
    url(r'^sync_log.html$', log_view.sync_log, name='sync_log'),
    url(r'^update_log.html$', log_view.update_log, name='update_log'),
    url(r'^show_download_log.html', log_view.show_download_log, name='show_download_log'),
    url(r'^show_download_log_list.html', log_view.show_download_log_list, name='show_download_log_list'),
    url(r'^download_log.html', log_view.download_log, name='download_log'),
]
