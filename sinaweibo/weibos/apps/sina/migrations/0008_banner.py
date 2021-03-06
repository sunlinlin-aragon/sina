# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-05 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0007_auto_20170914_0628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Banner \u6807\u9898')),
                ('banner_file', models.ImageField(max_length=128, upload_to='banner', verbose_name='\u56fe\u7247\u5730\u5740')),
                ('link', models.CharField(max_length=128, verbose_name='banner \u94fe\u63a5')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('is_send', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53d1\u5e03')),
            ],
        ),
    ]
