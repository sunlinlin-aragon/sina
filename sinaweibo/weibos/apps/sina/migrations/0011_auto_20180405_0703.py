# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-05 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0010_auto_20180405_0654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=64, unique=True, verbose_name='\u8003\u8bd5\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='examinationpointcategory',
            name='examination_point',
            field=models.ManyToManyField(blank=True, null=True, related_name='_examinationpointcategory_examination_point_+', to='sina.ExaminationPointCategory', verbose_name='\u8003\u70b9\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='examinationpointcategory',
            name='level',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=64, verbose_name='\u8003\u70b9\u7ea7\u522b'),
        ),
        migrations.AlterField(
            model_name='examinationpointcategory',
            name='title',
            field=models.CharField(max_length=64, unique=True, verbose_name='\u8003\u70b9\u7c7b\u522b\u540d\u79f0'),
        ),
    ]
