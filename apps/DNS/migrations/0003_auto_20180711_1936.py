# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-11 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DNS', '0002_auto_20180711_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bindrecord',
            name='bindzone',
        ),
        migrations.AddField(
            model_name='bindrecord',
            name='bindview',
            field=models.ManyToManyField(blank=True, null=True, to='DNS.BindView', verbose_name='\u6240\u5c5e\u89c6\u56fe'),
        ),
    ]
