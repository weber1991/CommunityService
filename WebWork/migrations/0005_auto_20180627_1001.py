# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-27 10:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebWork', '0004_toshixiang'),
    ]

    operations = [
        migrations.RenameField(
            model_name='toshixiang',
            old_name='wechctuser',
            new_name='wechatuser',
        ),
    ]