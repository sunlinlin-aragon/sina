# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-14 06:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0004_auto_20170914_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='send_datetime',
            field=models.DateTimeField(verbose_name='\u53d1\u9001\u65f6\u95f4'),
        ),
    ]