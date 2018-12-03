# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-13 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ticket', '0002_auto_20180809_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='BAssess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=3, verbose_name='评价等级')),
                ('content', models.TextField(verbose_name='评价内容')),
                ('addtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('changetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '评价内容',
                'verbose_name_plural': '评价内容',
            },
        ),
        migrations.AddField(
            model_name='bticket',
            name='assess',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Ticket.BAssess', verbose_name='票号评价'),
        ),
    ]
