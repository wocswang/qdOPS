# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser,Group
from django.db import models

# Create your models here.


class UserProfile(AbstractUser):
    """用户"""
    name = models.CharField(max_length=30,null=True,blank=True,validators="姓名")
    birthday = models.DateField(null=True,blank=True,verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    image = models.ImageField(upload_to="image/%Y/%m",default="image/default.png",max_length=100)

    class Meta:
        default_permissions=()
        permissions = (
            ('view_user','查看用户'),
            ('edit_user','管理用户'),

        )
        verbose_name="用户"
        verbose_name_plural="用户"

    def __unicode__(self):
        return self.username

class UserGroup(Group):
    group_name = models.CharField(max_length=32,unique=True,verbose_name=u"用户组")
    comment = models.TextField(blank=True,null=True,verbose_name=u"备注")

    def clean(self):
        self.name = self.group_name

    def __unicode__(self):
        return self.name
    class Meta:
        default_permissions=()
        permissions=(
            ('view_usergroup','查看用户组'),
            ('edit_usergroup','管理用户组'),

        )
        verbose_name="用户"
        verbose_name_plural="用户管理"




class LoginRecord(models.Model):
    user = models.CharField(max_length=32,verbose_name='用户')
    date = models.DateField(auto_now_add=True,verbose_name='时间')
    type = models.CharField(max_length=32,verbose_name="类型")
    action = models.CharField(max_length=32,verbose_name="动作")
    ip = models.CharField(max_length=15,verbose_name="用户IP")
    content = models.TextField(verbose_name='内容')

    def __unicode__(self):
        return self.user


    class Meta:
        default_permissions=()
        permissions =(
            ("view_loginrecord","查看登陆记录"),
            ("edit_loginrecord","管理登陆记录"),

        )
        ordering = ['-date']
        verbose_name="登陆信息"
        verbose_name_plural="登陆信息管理"
