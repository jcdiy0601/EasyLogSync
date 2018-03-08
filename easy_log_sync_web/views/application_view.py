#!/usr/bin/env python
# Author: 'JiaChen'

from django.shortcuts import render, redirect
from easy_log_sync_data import models
from easy_log_sync_web.forms import application_form
from utils import pagination
from utils.response import BaseResponse
from django.http import JsonResponse
import os
import shutil
from django.conf import settings
from utils.log import Logger
from django.contrib.auth.decorators import login_required


@login_required
def application_page(request):
    """应用视图"""
    current_page = request.GET.get("p", 1)
    current_page = int(current_page)
    application_obj_count = models.Application.objects.all().count()
    application_obj_list = models.Application.objects.all()
    page_obj = pagination.Page(current_page, application_obj_count)
    data = application_obj_list[page_obj.start:page_obj.end]
    page_str = page_obj.pager('application.html')
    return render(request, 'application.html', {'data': data, 'page_str': page_str})


@login_required
def application_add(request):
    """应用添加视图"""
    form_obj = application_form.ApplicationAddForm()
    if request.method == 'POST':
        form_obj = application_form.ApplicationAddForm(request.POST)
        if form_obj.is_valid():
            models.Application.objects.create(**form_obj.cleaned_data)
            project_obj = models.Project.objects.filter(id=form_obj.cleaned_data.get('project_id')).first()
            if not os.path.exists(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, form_obj.cleaned_data.get('path_name'))):
                os.mkdir(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, form_obj.cleaned_data.get('path_name')))
            Logger().log(message='[%s]添加应用[%s]成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('application.html')
        else:
            Logger().log(message='[%s]添加应用[%s]失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'application_add.html', {'form_obj': form_obj})
    return render(request, 'application_add.html', {'form_obj': form_obj})


@login_required
def application_del(request):
    """应用删除视图"""
    response = BaseResponse()
    if request.method == 'POST':
        aid = request.POST.get('aid')
        try:
            application_obj = models.Application.objects.filter(id=aid).first()
            application_name = application_obj.name
            project_obj = models.Project.objects.filter(id=application_obj.project_id).first()
            if os.path.exists(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, application_obj.path_name)):
                shutil.rmtree(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, application_obj.path_name))
            application_obj.delete()
            response.message = '删除成功'
            Logger().log(message='[%s]删除应用[%s]成功' % (request.user.name, application_name), mode=True)
        except Exception as e:
            response.status = False
            response.message = '删除失败'
            response.error = str(e)
            Logger().log(message='[%s]删除应用失败,%s' % (request.user.name, str(e)), mode=False)
        return JsonResponse(response.__dict__)


@login_required
def application_edit(request, *args, **kwargs):
    """应用编辑视图"""
    aid = kwargs['aid']
    form_obj = application_form.ApplicationEditForm(initial={'aid': aid})
    if request.method == 'POST':
        form_obj = application_form.ApplicationEditForm(data=request.POST, initial={'aid': aid})
        if form_obj.is_valid():
            application_obj = models.Application.objects.filter(id=aid).first()
            project_obj = models.Project.objects.filter(id=application_obj.project_id).first()
            if os.path.exists(os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, application_obj.path_name)):
                os.rename(
                    os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, application_obj.path_name),
                    os.path.join(settings.RSYNC_LOG_DIR, project_obj.path_name, form_obj.cleaned_data.get('path_name'))
                )
            models.Application.objects.filter(id=aid).update(**form_obj.cleaned_data)
            Logger().log(message='[%s]编辑应用[%s]成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('application.html')
        else:
            Logger().log(message='[%s]编辑应用[%s]失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'application_edit.html', {'form_obj': form_obj, 'aid': aid})
    return render(request, 'application_edit.html', {'form_obj': form_obj, 'aid': aid})
