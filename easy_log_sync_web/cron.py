#!/usr/bin/env python
# Author: 'JiaChen'

from easy_log_sync_data import models
from utils.log import Logger
import subprocess
import os
from django.conf import settings


def rsync_app():
    """
    每天同步日志视图
    :return:
    """
    application_list = models.Application.objects.all()
    for application_obj in application_list:
        application_path_name = application_obj.path_name
        project_path_name = application_obj.project.path_name
        receive_path = os.path.join(settings.RSYNC_LOG_DIR, project_path_name, application_path_name)
        module_name = '%s_%s' % (project_path_name, application_path_name)
        ip = application_obj.ip
        command = '/usr/bin/rsync -az --delete --password-file=/etc/easylogrsync.secrets easylogrsync_user@%s::%s %s' % (ip,
                                                                                                                         module_name,
                                                                                                                         receive_path)
        try:
            subprocess.call(command, shell=True)
            Logger().log(message='计划任务执行更新成功,%s[%s]已更新' % (application_obj.project.name,
                                                           application_obj.name),
                         mode=True)
        except Exception as e:
            Logger().log(message='计划任务执行更新失败,%s[%s]更新失败,%s' % (application_obj.project.name,
                                                               application_obj.name,
                                                               str(e)),
                         mode=False)
