#!/usr/bin/env python
# Author: JiaChen

from django.contrib.auth.decorators import login_required
from utils.response import BaseResponse
from easy_log_sync_data import models
from django.http import JsonResponse


@login_required
def chart1(request):
    """
    仪表盘图1视图
    :param request:
    :return:
    """
    response = BaseResponse()
    ret = {}
    project_count = models.Project.objects.all().count()
    application_count = models.Application.objects.all().count()
    user_count = models.UserProfile.objects.all().count()
    ret['project_count'] = project_count
    ret['application_count'] = application_count
    ret['user_count'] = user_count
    response.data = ret
    return JsonResponse(response.__dict__)
