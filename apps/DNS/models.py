# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import binascii
import socket
from cryptography.fernet import Fernet, InvalidToken
import dns.exception
import dns.query
import dns.tsig
import dns.zone
from django.conf import settings
from DNS import exceptions
from django.db import models
# Register your models here.


TSIG_ALGORITHMS = (('HMAC-MD5.SIG-ALG.REG.INT', 'MD5'),
                   ('hmac-sha1', 'SHA1'),
                   ('hmac-sha256', 'SHA256'),
                   ('hmac-sha384', 'SHA384'),
                   ('hmac-sha512', 'SHA512'))


class Key(models.Model):
    """key管理"""
    name = models.CharField(max_length=255,unique=True,verbose_name="KEY名称")
    data = models.CharField(max_length=255,verbose_name="私钥")
    algorithm = models.CharField(max_length=255,choices=TSIG_ALGORITHMS,verbose_name="私钥加密")


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]






class BindRecord(models.Model):
    """Bind record管理"""

    bindzone=models.ManyToManyField('BindZone',blank=True,null=True,verbose_name="所属域")
    bindview = models.ManyToManyField('BindView',blank=True,null=True,verbose_name="所属视图")
    name =models.CharField(max_length=255,verbose_name="名称")
    Type = models.CharField(max_length=50,choices=settings.RECORD_TYPE_CHOICES,verbose_name="类型")
    ttl = models.IntegerField(choices=settings.TTL_CHOICES, verbose_name="ttl")
    Data = models.GenericIPAddressField(verbose_name="IP")

    def __unicode__(self):
        return self.name


    class Meta:
        default_permissions=()
        permissions = (
            ("can_read_bind_records","读取域名记录权限"),
            ("can_change_bind_records","更改域名记录权限"),
            ("can_add_bind_records","添加域名记录权限"),
            ("can_delete_bind_records","删除域名记录权限"),
        )
        verbose_name="record管理"
        verbose_name_plural=verbose_name
        #unique_together = ['bindzone','name']


class BindZone(models.Model):
    """Bind zone管理"""
    zonename = models.CharField(max_length=255,verbose_name="二级域名")

    def __unicode__(self):
        return self.zonename

    class Meta:
        verbose_name = "zone管理"
        verbose_name_plural=verbose_name


class BindView(models.Model):
    """Bind view管理"""
    default_transfer_view = models.ManyToManyField(BindZone, verbose_name="所属域")
    default_transfer_key = models.OneToOneField(Key, verbose_name="所属密钥")
    viewname = models.CharField(max_length=255,unique=True,verbose_name="视图名称")
    server = models.ForeignKey('BindServer', verbose_name='server')
    name=models.CharField(max_length=255,unique=True,verbose_name="名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name="view管理"
        verbose_name_plural=verbose_name


class BindServer(models.Model):
    """Bind server管理"""

    hostname = models.CharField(max_length=255,unique=True,verbose_name="bindIP")
    dns_port = models.IntegerField(default=53,
                                   verbose_name="DNS port",
                                   help_text="The port where the BIND server is listening for DNS "
                                             "requests. binder especially uses that port for the dynamic "
                                             "zone updates. In most cases you should always leave it at the "
                                             "default port 53.")

    def __unicode__(self):
        return self.hostname

    class Meta:
        verbose_name="server管理"
        verbose_name_plural=verbose_name
