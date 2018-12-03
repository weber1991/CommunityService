# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-13 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BAdmin', '0002_communitybase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitybase',
            name='keep1',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='保留1'),
        ),
        migrations.AlterField(
            model_name='communitybase',
            name='keep2',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='保留2'),
        ),
        migrations.AlterField(
            model_name='communitybase',
            name='keep3',
            field=models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='保留3'),
        ),
    ]
