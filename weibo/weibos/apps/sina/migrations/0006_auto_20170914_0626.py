# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-14 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0005_auto_20170914_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(blank=True, max_length=64, null=True, upload_to=b'/weibos/media/', verbose_name='\u56fe\u7247\u5730\u5740'),
        ),
    ]
