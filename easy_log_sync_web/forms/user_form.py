#!/usr/bin/env python
# Author: 'JiaChen'

from django import forms
from django.forms import fields
from django.forms import widgets
from easy_log_sync_data import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class UserAddForm(forms.Form):
    """添加用户表单认证"""
    email = fields.EmailField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='邮箱',
        help_text='必填项',
        widget=widgets.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='姓名',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='密码',
        help_text='必填项',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        n = models.UserProfile.objects.filter(email=self.cleaned_data.get('email')).count()
        if not n:
            return self.cleaned_data.get('email')
        else:
            raise ValidationError(_('邮箱[%(email)s]已存在'), code='invalid', params={'email': email})


class UserEditForm(forms.Form):
    """编辑用户表单认证"""
    email = fields.EmailField(
        error_messages={'required': '不能为空', 'invalid': '格式错误'},
        label='邮箱',
        help_text='必填项',
        widget=widgets.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    name = fields.CharField(
        max_length=64,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于64位'},
        label='姓名',
        help_text='必填项',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_obj = models.UserProfile.objects.get(id=self.uid)
        n = models.UserProfile.objects.exclude(email=user_obj.email).filter(
            email=self.cleaned_data.get('email')).count()
        if not n:
            return self.cleaned_data.get('email')
        else:
            raise ValidationError(_('邮箱%(email)s已存在'), code='invalid', params={'email': email})

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.uid = self.initial['uid']
        user_obj = models.UserProfile.objects.get(id=self.uid)
        self.fields['email'].initial = user_obj.email
        self.fields['name'].initial = user_obj.name


class UserChangePass(forms.Form):
    """重置密码视图表单验证类"""
    password = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='密码',
        help_text='必填项',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = fields.CharField(
        max_length=128,
        error_messages={'required': '不能为空', 'invalid': '格式错误', 'max_length': '最大长度不能大于128位'},
        label='确认密码',
        help_text='必填项',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError(_('两次输入的密码不一致'), code='invalid')
        else:
            return self.cleaned_data
