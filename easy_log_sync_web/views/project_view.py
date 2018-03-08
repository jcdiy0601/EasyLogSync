#!/usr/bin/env python
# Author: 'JiaChen'

from django.shortcuts import render, redirect
from easy_log_sync_data import models
from easy_log_sync_web.forms import project_form
from utils import pagination
from utils.response import BaseResponse
from django.http import JsonResponse
import os
import shutil
from django.conf import settings
from utils.log import Logger
from django.contrib.auth.decorators import login_required


@login_required
def project_page(request):
    """项目视图"""
    current_page = request.GET.get("p", 1)
    current_page = int(current_page)
    project_obj_count = models.Project.objects.all().count()
    project_obj_list = models.Project.objects.all()
    page_obj = pagination.Page(current_page, project_obj_count)
    data = project_obj_list[page_obj.start:page_obj.end]
    page_str = page_obj.pager('project.html')
    return render(request, 'project.html', {'data': data, 'page_str': page_str})


@login_required
def project_add(request):
    """项目添加视图"""
    form_obj = project_form.ProjectAddForm()
    if request.method == 'POST':
        form_obj = project_form.ProjectAddForm(request.POST)
        if form_obj.is_valid():
            models.Project.objects.create(**form_obj.cleaned_data)
            if not os.path.exists(os.path.join(settings.RSYNC_LOG_DIR, form_obj.cleaned_data.get('path_name'))):
                os.mkdir(os.path.join(settings.RSYNC_LOG_DIR, form_obj.cleaned_data.get('path_name')))
            Logger().log(message='[%s]添加项目[%s]成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('project.html')
        else:
            Logger().log(message='[%s]添加项目[%s]失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'project_add.html', {'form_obj': form_obj})
    return render(request, 'project_add.html', {'form_obj': form_obj})


@login_required
def project_del(request):
    """项目删除视图"""
    response = BaseResponse()
    if request.method == 'POST':
        pid = request.POST.get('pid')
        try:
            project_obj = models.Project.objects.filter(id=pid).first()
            project_name = project_obj.name
            if os.path.exists(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name)):
                shutil.rmtree(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name))
            project_obj.delete()
            response.message = '删除成功'
            Logger().log(message='[%s]删除项目[%s]成功' % (request.user.name, project_name), mode=True)
        except Exception as e:
            response.status = False
            response.message = '删除失败'
            response.error = str(e)
            Logger().log(message='[%s]删除项目失败,%s' % (request.user.name, str(e)), mode=False)
        return JsonResponse(response.__dict__)


@login_required
def project_edit(request, *args, **kwargs):
    """项目编辑视图"""
    pid = kwargs['pid']
    form_obj = project_form.ProjectEditForm(initial={'pid': pid})
    if request.method == 'POST':
        form_obj = project_form.ProjectEditForm(data=request.POST, initial={'pid': pid})
        if form_obj.is_valid():
            project_obj = models.Project.objects.filter(id=pid).first()
            if os.path.exists(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name)):
                os.rename(
                    os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name),
                    os.path.join(settings.RSYNC_LOG_DIR, form_obj.cleaned_data.get('path_name'))
                )
            models.Project.objects.filter(id=pid).update(**form_obj.cleaned_data)
            Logger().log(message='[%s]编辑项目[%s]成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('project.html')
        else:
            Logger().log(message='[%s]编辑项目[%s]失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'project_edit.html', {'form_obj': form_obj, 'pid': pid})
    return render(request, 'project_edit.html', {'form_obj': form_obj, 'pid': pid})
