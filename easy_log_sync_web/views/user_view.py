#!/usr/bin/env python
# Author: 'JiaChen'

from django.shortcuts import render, redirect
from easy_log_sync_data import models
from easy_log_sync_web.forms import user_form
from utils import pagination
from utils.response import BaseResponse
from django.http import JsonResponse
from utils.log import Logger
from django.contrib.auth.decorators import login_required


@login_required
def user_page(request):
    """用户视图"""
    current_page = request.GET.get("p", 1)
    current_page = int(current_page)
    user_obj_count = models.UserProfile.objects.all().count()
    user_obj_list = models.UserProfile.objects.all()
    page_obj = pagination.Page(current_page, user_obj_count)
    data = user_obj_list[page_obj.start:page_obj.end]
    page_str = page_obj.pager('user.html')
    return render(request, 'user.html', {'data': data, 'page_str': page_str})


@login_required
def user_add(request):
    """用户添加视图"""
    form_obj = user_form.UserAddForm()
    if request.method == 'POST':
        form_obj = user_form.UserAddForm(request.POST)
        if form_obj.is_valid():
            email = form_obj.cleaned_data.get('email')
            name = form_obj.cleaned_data.get('name')
            password = form_obj.cleaned_data.get('password')
            user_obj = models.UserProfile.objects.create(email=email, name=name, is_admin=False, is_active=True, is_superuser=False)
            user_obj.set_password(password)
            user_obj.save()
            Logger().log(message='[%s]添加用户[%s]成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('user.html')
        else:
            Logger().log(message='[%s]添加用户[%s]失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'user_add.html', {'form_obj': form_obj})
    return render(request, 'user_add.html', {'form_obj': form_obj})


@login_required
def user_del(request):
    """用户删除视图"""
    response = BaseResponse()
    if request.method == 'POST':
        uid = request.POST.get('uid')
        try:
            user_obj = models.UserProfile.objects.filter(id=uid).first()
            user_name = user_obj.name
            user_obj.delete()
            response.message = '删除成功'
            Logger().log(message='[%s]删除用户[%s]成功' % (request.user.name, user_name), mode=True)
        except Exception as e:
            response.status = False
            response.message = '删除失败'
            response.error = str(e)
            Logger().log(message='[%s]删除用户失败,%s' % (request.user.name, str(e)), mode=False)
        return JsonResponse(response.__dict__)
    

@login_required
def user_edit(request, *args, **kwargs):
    """项目编辑视图"""
    uid = kwargs['uid']
    form_obj = user_form.UserEditForm(initial={'uid': uid})
    if request.method == 'POST':
        form_obj = user_form.UserEditForm(data=request.POST, initial={'uid': uid})
        if form_obj.is_valid():
            models.UserProfile.objects.filter(id=uid).update(**form_obj.cleaned_data)
            Logger().log(message='[%s]编辑用户[%s]成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('user.html')
        else:
            Logger().log(message='[%s]编辑用户[%s]失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'user_edit.html', {'form_obj': form_obj, 'uid': uid})
    return render(request, 'user_edit.html', {'form_obj': form_obj, 'uid': uid})


@login_required
def user_change_pass(request, *args, **kwargs):
    """修改用户密码视图"""
    uid = kwargs['uid']
    if request.method == 'GET':
        form_obj = user_form.UserChangePass()
        return render(request, 'user_change_pass.html', {'form_obj': form_obj, 'uid': uid})
    elif request.method == 'POST':
        form_obj = user_form.UserChangePass(request.POST)
        if form_obj.is_valid():
            password = form_obj.cleaned_data.get('password')
            user_obj = models.UserProfile.objects.get(id=uid)
            user_obj.set_password(password)
            user_obj.save()
            Logger().log(message='[%s]重置[%s]密码成功' % (request.user.name, form_obj.cleaned_data.get('name')), mode=True)
            return redirect('/log_web/user.html')
        else:
            Logger().log(message='[%s]重置[%s]密码失败' % (request.user.name, request.POST.get('name')), mode=False)
            return render(request, 'user_change_pass.html', {'form_obj': form_obj, 'uid': uid})


@login_required
def user_relevance_application(request, *args, **kwargs):
    """关联应用视图"""
    uid = kwargs['uid']
    user_obj = models.UserProfile.objects.get(id=uid)
    all_application_list = list(models.Application.objects.values('id', 'name'))
    for item in all_application_list:
        item['name'] = str(models.Application.objects.filter(id=item['id']).first().project.name) + '-' + item['name']
    user_application_list = list(user_obj.app.values('id', 'name'))
    for item in user_application_list:
        item['name'] = str(models.Application.objects.filter(id=item['id']).first().project.name) + '-' + item['name']
    sub_application_list = []
    for item in all_application_list:
        if item not in user_application_list:
            sub_application_list.append(item)
    if request.method == 'POST':
        try:
            application_list = request.POST.getlist('application')
            user_obj.app.set(application_list)
            Logger().log(message='[%s]关联应用%s成功' % (user_obj.name, application_list), mode=True)
            return redirect('/log_web/user.html')
        except Exception as e:
            error = str(e)
            Logger().log(message='[%s]关联应用%s失败,%s' % (user_obj.name, request.POST.getlist('application'), error), mode=False)
            return render(request, 'user_relevance_application.html', {'uid': uid,
                                                                       'sub_application_list': sub_application_list,
                                                                       'user_application_list': user_application_list,
                                                                       'error': error})
    return render(request, 'user_relevance_application.html', {'uid': uid,
                                                               'sub_application_list': sub_application_list,
                                                               'user_application_list': user_application_list})