#!/usr/bin/env python
# Author: 'JiaChen'

from django import forms
from django.forms import fields
from django.forms import widgets
from easy_log_sync_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class ApplicationAddForm(forms.Form):
    """添加应用表单认证"""
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='应用名称',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    path_name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='应用目录名',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='IP地址',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    project_id = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='所属项目',
        help_text='必填',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(ApplicationAddForm, self).__init__(*args, **kwargs)
        self.fields['project_id'].widget.choices = list(models.Project.objects.values_list('id', 'name'))
        self.fields['project_id'].initial = []

    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = models.Application.objects.filter(name=name).count()
        if count:
            raise ValidationError(_('应用名称[%(name)s]已存在'), code='invalid', params={'name': name})
        return name

    def clean_project_id(self):
        project_id = self.cleaned_data.get('project_id')
        count = models.Project.objects.filter(id=project_id).count()
        if not count:
            raise ValidationError(_('所属项目[%(project_id)s]不存在'), code='invalid', params={'project_id': project_id})
        return project_id


class ApplicationEditForm(forms.Form):
    """编辑应用表单认证"""
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='应用名称',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    path_name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='应用目录名',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    ip = fields.GenericIPAddressField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='IP地址',
        help_text='必填',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    project_id = fields.IntegerField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='所属项目',
        help_text='必填',
        widget=widgets.Select(
            choices=[],
            attrs={'class': 'form-control'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(ApplicationEditForm, self).__init__(*args, **kwargs)
        self.aid = self.initial['aid']
        application_obj = models.Application.objects.filter(id=self.aid).first()
        self.fields['name'].initial = application_obj.name
        self.fields['path_name'].initial = application_obj.path_name
        self.fields['ip'].initial = application_obj.ip
        self.fields['project_id'].widget.choices = list(models.Project.objects.values_list('id', 'name'))
        self.fields['project_id'].initial = [application_obj.project_id]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = models.Application.objects.exclude(id=self.aid).filter(name=name).count()
        if count:
            raise ValidationError(_('应用名称[%(name)s]已存在'), code='invalid', params={'name': name})
        return name

    def clean_project_id(self):
        project_id = self.cleaned_data.get('project_id')
        count = models.Project.objects.filter(id=project_id).count()
        if not count:
            raise ValidationError(_('所属项目[%(project_id)s]不存在'), code='invalid', params={'project_id': project_id})
        return project_id
