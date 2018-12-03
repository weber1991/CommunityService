# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-03 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BAdmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityBase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('author', models.CharField(max_length=255, verbose_name='作者')),
                ('keep1', models.CharField(default='', max_length=512, verbose_name='保留1')),
                ('keep2', models.CharField(default='', max_length=512, verbose_name='保留2')),
                ('keep3', models.CharField(default='', max_length=512, verbose_name='保留3')),
            ],
            options={
                'verbose_name': '基础信息表',
                'verbose_name_plural': '基础信息表',
            },
        ),
    ]