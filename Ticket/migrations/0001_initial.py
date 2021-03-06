# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-09 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BUser', '0004_auto_20180809_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brandonnumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255, verbose_name='随机号码')),
                ('state', models.BooleanField(default=False, verbose_name='使用状态')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('hold0', models.CharField(max_length=255, null=True, verbose_name='保留')),
                ('hold1', models.CharField(max_length=255, null=True, verbose_name='保留')),
                ('hold2', models.CharField(max_length=255, null=True, verbose_name='保留')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '随机码',
                'verbose_name_plural': '随机码',
            },
        ),
        migrations.CreateModel(
            name='BService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=3, verbose_name='业务类型')),
                ('name', models.CharField(max_length=255, verbose_name='业务名称')),
                ('window', models.CharField(blank=True, max_length=255, null=True, verbose_name='窗口名称')),
                ('state', models.CharField(max_length=125, verbose_name='业务状态')),
                ('note', models.CharField(max_length=255, null=True, verbose_name='备注')),
                ('hold0', models.CharField(max_length=255, null=True, verbose_name='保留1')),
                ('hold1', models.CharField(max_length=255, null=True, verbose_name='保留2')),
                ('hold2', models.CharField(max_length=255, null=True, verbose_name='保留3')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '业务',
                'verbose_name_plural': '业务',
            },
        ),
        migrations.CreateModel(
            name='BTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=6, verbose_name='票号')),
                ('type', models.BooleanField(default=False, verbose_name='票号类型')),
                ('queuetime', models.DateTimeField(null=True, verbose_name='预约时间')),
                ('starttime', models.DateTimeField(null=True, verbose_name='取号时间')),
                ('dotime', models.DateTimeField(null=True, verbose_name='办理时间')),
                ('endtime', models.DateTimeField(null=True, verbose_name='办结时间')),
                ('outtime', models.DateTimeField(null=True, verbose_name='作废时间')),
                ('state', models.IntegerField(default=0, verbose_name='票号状态')),
                ('note', models.TextField(default='备注：每条成功取号信息，除了要显示当前号数以及叫号情况之外，还要提示过号后每个号将延迟两个号再进行业务办理。', verbose_name='备注')),
                ('hold0', models.CharField(max_length=255, null=True, verbose_name='保留')),
                ('hold1', models.CharField(max_length=255, null=True, verbose_name='保留')),
                ('hold2', models.CharField(max_length=255, null=True, verbose_name='保留')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticket.BService', verbose_name='业务')),
            ],
            options={
                'verbose_name': '票号',
                'verbose_name_plural': '票号',
                'ordering': ['starttime'],
            },
        ),
        migrations.CreateModel(
            name='BUser2Window',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BUser.BUser', verbose_name='办理人')),
            ],
            options={
                'verbose_name': '人员窗口关系表',
                'verbose_name_plural': '人员窗口关系表',
            },
        ),
        migrations.CreateModel(
            name='BWindow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='窗口名称')),
                ('address', models.CharField(max_length=255, verbose_name='窗口地址')),
                ('orderid', models.IntegerField(default=100, verbose_name='排序号')),
                ('show', models.TextField(blank=True, null=True, verbose_name='窗口介绍')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('hold0', models.CharField(max_length=255, verbose_name='保留事项')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '窗口',
                'verbose_name_plural': '窗口',
                'ordering': ['orderid'],
            },
        ),
        migrations.CreateModel(
            name='BWindow2Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticket.BService', verbose_name='业务')),
                ('window', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticket.BWindow', verbose_name='窗口号')),
            ],
            options={
                'verbose_name': '窗口与业务关系表',
                'verbose_name_plural': '窗口与业务关系表',
            },
        ),
        migrations.AddField(
            model_name='buser2window',
            name='window',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ticket.BWindow', verbose_name='对应窗口'),
        ),
        migrations.AddField(
            model_name='bticket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ticket.BUser2Window', verbose_name='办理人及窗口'),
        ),
        migrations.AddField(
            model_name='bticket',
            name='wechatuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BUser.BWechatUser', verbose_name='取号人'),
        ),
    ]
