#!/usr/bin/env python
# Author: 'JiaChen'

from django import forms
from django.forms import fields
from django.forms import widgets
from easy_log_sync_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class ProjectAddForm(forms.Form):
    """添加项目表单认证"""
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='项目名称',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    path_name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='项目目录名',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = models.Project.objects.filter(name=name).count()
        if count:
            raise ValidationError(_('项目名称[%(name)s]已存在'), code='invalid', params={'name': name})
        return name

    def clean_path_name(self):
        path_name = self.cleaned_data.get('path_name')
        count = models.Project.objects.filter(path_name=path_name).count()
        if count:
            raise ValidationError(_('项目目录名[%(path_name)s]已存在'), code='invalid', params={'path_name': path_name})
        return path_name


class ProjectEditForm(forms.Form):
    """编辑项目表单认证"""
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='项目名称',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    path_name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='项目目录名',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(ProjectEditForm, self).__init__(*args, **kwargs)
        self.pid = self.initial['pid']
        project_obj = models.Project.objects.filter(id=self.pid).first()
        self.fields['name'].initial = project_obj.name
        self.fields['path_name'].initial = project_obj.path_name

    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = models.Project.objects.exclude(id=self.pid).filter(name=name).count()
        if count:
            raise ValidationError(_('项目名称[%(name)s]已存在'), code='invalid', params={'name': name})
        return name

    def clean_path_name(self):
        path_name = self.cleaned_data.get('path_name')
        count = models.Project.objects.exclude(id=self.pid).filter(path_name=path_name).count()
        if count:
            raise ValidationError(_('项目目录名[%(path_name)s]已存在'), code='invalid', params={'path_name': path_name})
        return path_name
