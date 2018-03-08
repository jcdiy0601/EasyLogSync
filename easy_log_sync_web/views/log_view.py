#!/usr/bin/env python
# Author: 'JiaChen'

from django.shortcuts import render
from easy_log_sync_data import models
from django.http import FileResponse
from utils.response import BaseResponse
from django.http import JsonResponse
from utils.log import Logger
from django.contrib.auth.decorators import login_required
import subprocess
import os
from django.conf import settings
from utils.filter_log import post_file, cut_file_list
from django.views.decorators.csrf import csrf_exempt
import tempfile
import zipfile
from utils.pager import PageInfo


@login_required
def sync_log(request):
    """同步日志视图"""
    user_obj = request.user
    user_application_list = list(user_obj.app.values('id', 'name'))
    name_list = []
    result_list = []
    for item in user_application_list:
        item['name'] = str(models.Application.objects.filter(id=item['id']).first().project.name) + '-' + item['name']
        name_list.append(item['name'])
    name_list.sort()
    for name in name_list:
        for item in user_application_list:
            if name == item['name']:
                result_list.append(item)
    return render(request, 'sync_log.html', {'result_list': result_list})


def update_log(request):
    """更新日志视图"""
    response = BaseResponse()
    if request.method == 'POST':
        app_value = request.POST.get('app_value')
        application_obj = models.Application.objects.filter(id=app_value).first()
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
            response.message = '更新成功!'
            Logger().log(message='[%s]执行更新命令成功,%s[%s]已更新' % (request.user.name,
                                                             application_obj.project.name,
                                                             application_obj.name),
                         mode=True)
        except Exception as e:
            response.status = False
            response.error = str(e)
            response.message = '更新失败!'
            Logger().log(message='[%s]执行更新命令失败,%s[%s]未能成功更新,%s' % (request.user.name,
                                                                   application_obj.project.name,
                                                                   application_obj.name,
                                                                   str(e)),
                         mode=False)
        return JsonResponse(response.__dict__)


@login_required
def show_download_log(request):
    """
    显示可下载日志视图
    :param request:
    :return:
    """
    user_obj = request.user
    user_application_list = list(user_obj.app.values('id', 'name'))
    name_list = []
    result_list = []
    for item in user_application_list:
        item['name'] = str(models.Application.objects.filter(id=item['id']).first().project.name) + '-' + item['name']
        name_list.append(item['name'])
    name_list.sort()
    for name in name_list:
        for item in user_application_list:
            if name == item['name']:
                result_list.append(item)
    return render(request, 'show_download_log.html', {'result_list': result_list})


def show_download_log_list(request):
    """
    显示要下载的日志列表视图
    :param request:
    :return:
    """
    response = BaseResponse()
    try:
        ret = {}
        choice_value = request.GET.get('choiceValue')
        project_name = choice_value.split('-')[0]
        application_name = choice_value.split('-')[1]
        project_path = models.Project.objects.filter(name=project_name).first().path_name
        application_path = models.Application.objects.filter(name=application_name).first().path_name
        abs_path = os.path.join(settings.RSYNC_LOG_DIR, project_path, application_path)
        ret_list = post_file(abs_path)
        file_count = len(cut_file_list(application_path, ret_list))
        page_info = PageInfo(request.GET.get('pager', None), file_count)
        ret['data_list'] = cut_file_list(application_path, ret_list)[page_info.start: page_info.end]
        ret['page_info'] = {
            'page_str': page_info.pager(),
            'page_start': page_info.start
        }
        response.data = ret
        Logger().log(message='[%s]显示要下载的日志列表成功,路径为[%s]' % (request.user.name, abs_path), mode=True)
    except Exception as e:
        response.status = False
        response.message = '查询失败'
        response.error = str(e)
        Logger().log(message='[%s]显示要下载的日志列表失败,%s' % (request.user.name, str(e)), mode=False)
    return JsonResponse(response.__dict__)


@csrf_exempt
def download_log(request):
    """
    下载视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        download_file_path = request.POST.get('download_file_path')
        try:
            os.chdir(os.path.dirname(download_file_path))
            temp = tempfile.TemporaryFile(dir=os.path.dirname(download_file_path))
            archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
            archive.write(os.path.basename(download_file_path))
            archive.close()
            response = FileResponse(temp)
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment; filename=%s.zip' % os.path.basename(download_file_path)
            response['Content-Length'] = temp.tell()
            temp.seek(0)
            Logger().log(message='[%s]下载日志[%s]成功' % (request.user.name, download_file_path), mode=True)
            return response
        except Exception as e:
            Logger().log(message='[%s]下载日志[%s]失败,%s' % (request.user.name, download_file_path, str(e)), mode=False)