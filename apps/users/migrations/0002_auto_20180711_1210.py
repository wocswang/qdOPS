# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-11 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, verbose_name='\u7528\u6237')),
                ('date', models.DateField(auto_now_add=True, verbose_name='\u65f6\u95f4')),
                ('type', models.CharField(max_length=32, verbose_name='\u7c7b\u578b')),
                ('action', models.CharField(max_length=32, verbose_name='\u52a8\u4f5c')),
                ('ip', models.CharField(max_length=15, verbose_name='\u7528\u6237IP')),
                ('content', models.TextField(verbose_name='\u5185\u5bb9')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name_plural': '\u767b\u9646\u4fe1\u606f\u7ba1\u7406',
                'default_permissions': (),
                'verbose_name': '\u767b\u9646\u4fe1\u606f',
                'permissions': (('view_loginrecord', '\u67e5\u770b\u767b\u9646\u8bb0\u5f55'), ('edit_loginrecord', '\u7ba1\u7406\u767b\u9646\u8bb0\u5f55')),
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('group_name', models.CharField(max_length=32, unique=True, verbose_name='\u7528\u6237\u7ec4')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='\u5907\u6ce8')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237\u7ba1\u7406',
                'permissions': (('view_usergroup', '\u67e5\u770b\u7528\u6237\u7ec4'), ('edit_usergroup', '\u7ba1\u7406\u7528\u6237\u7ec4')),
            },
            bases=('auth.group',),
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'default_permissions': (), 'permissions': (('view_user', '\u67e5\u770b\u7528\u6237'), ('edit_user', '\u7ba1\u7406\u7528\u6237')), 'verbose_name': '\u7528\u6237', 'verbose_name_plural': '\u7528\u6237'},
        ),
    ]