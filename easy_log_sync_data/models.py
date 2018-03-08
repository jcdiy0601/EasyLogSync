from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('用户必须有一个email地址')
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self.db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """用户表"""
    email = models.EmailField(verbose_name='邮箱', unique=True)
    name = models.CharField(verbose_name='姓名', max_length=64)
    is_active = models.BooleanField(verbose_name='是否可登录', default=True)
    is_admin = models.BooleanField(verbose_name='是否为管理员', default=False)

    # class Meta:
    #     verbose_name_plural = '用户表'
    #     permissions = (
    #         ('can_show_user', '可以访问用户管理页面'),
    #         ('can_show_add_user', '可以访问添加用户页面'),
    #         ('can_add_user', '可以添加用户'),
    #         ('can_delete_user', '可以删除用户'),
    #         ('can_show_edit_user', '可以访问用户编辑页面'),
    #         ('can_edit_user', '可以编辑用户'),
    #         ('can_show_change_pass_user', '可以访问重置密码页面'),
    #         ('can_change_pass_user', '可以重置密码'),
    #         ('can_show_change_permission_user', '可以访问修改用户权限页面'),
    #         ('can_change_permission_user', '可以修改用户权限'),
    #     )
    class Meta:
        verbose_name_plural = '用户表'

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        # __unicode__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     # Does the user have a specific permission?
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     # Does the user have permissions to view the app `app_label`?
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_staff(self):
        # Is the user a member of staff?
        # Simplest possible answer: All admins are staff
        return self.is_active


class Project(models.Model):
    """项目表"""
    name = models.CharField(verbose_name='项目名称', max_length=64, unique=True)
    path_name = models.CharField(verbose_name='项目目录名', max_length=64, unique=True)

    class Meta:
        verbose_name_plural = '项目表'

    def __str__(self):
        return self.name


class Application(models.Model):
    """应用表"""
    name = models.CharField(verbose_name='应用名称', max_length=64, unique=True)
    path_name = models.CharField(verbose_name='应用目录名', max_length=64)
    ip = models.GenericIPAddressField(verbose_name='IP地址')
    project = models.ForeignKey(verbose_name='所属项目', to='Project')
    userprofile = models.ManyToManyField(verbose_name='所属用户', to='UserProfile', related_name='app')

    class Meta:
        verbose_name_plural = '应用表'

    def __str__(self):
        return self.name
