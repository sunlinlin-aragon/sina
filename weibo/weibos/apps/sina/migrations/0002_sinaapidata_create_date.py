# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-14 03:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sina', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sinaapidata',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]