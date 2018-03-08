#!/usr/bin/env python
# Author: 'JiaChen'

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def serialize_project_url(project_obj):
    """
    初始化项目编辑、删除url
    :param project_obj: 项目实例
    :return:
    """
    tmp = '<a href="/log_web/project_edit_%s.html" class="btn btn-xs btn-success">编辑</a>' % project_obj.id + ' | ' + '<button pid="%s" class="btn btn-xs btn-danger" tag="del-tag">删除</button>' % project_obj.id
    return mark_safe(tmp)


@register.simple_tag
def serialize_application_url(application_obj):
    """
    初始化应用编辑、删除url
    :param application_obj: 应用实例
    :return:
    """
    tmp = '<a href="/log_web/application_edit_%s.html" class="btn btn-xs btn-success">编辑</a>' % application_obj.id + ' | ' + '<button aid="%s" class="btn btn-xs btn-danger" tag="del-tag">删除</button>' % application_obj.id
    return mark_safe(tmp)


@register.simple_tag
def serialize_user_url(user_obj):
    """
    初始化用户编辑、删除url
    :param user_obj:
    :return:
    """
    tmp = '<a href="/log_web/user_edit_%s.html" class="btn btn-xs btn-success">编辑</a>' % user_obj.id + \
          ' | ' + '<button uid="%s" class="btn btn-xs btn-danger" tag="del-tag">删除</button>' % user_obj.id + \
          ' | ' + '<a href="/log_web/user_change_pass_%s.html" class="btn btn-xs btn-warning">重置密码</a>' % user_obj.id +\
          ' | ' + '<a href="/log_web/user_relevance_application_%s.html" class="btn btn-xs btn-pink">关联应用</a>' % user_obj.id
    return mark_safe(tmp)
