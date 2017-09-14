# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict


# Create your models here.


class SinaApiData(models.Model):
    code = models.CharField(max_length=64, verbose_name='sina code', blank=True, null=True)
    token = models.CharField(max_length=64, verbose_name='access token', blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token


class Article(models.Model):
    title = models.CharField(max_length=32, verbose_name='文章标题')
    content = models.TextField(max_length=10000, verbose_name='正文内容')
    cover = models.ImageField(upload_to='article', blank=True, null=True, verbose_name='图片地址', max_length=64)
    summary = models.CharField(max_length=64, verbose_name='文章导语')
    text = models.CharField(max_length=1900, verbose_name='与其绑定短微博内容')

    send_datetime = models.DateTimeField(verbose_name='发送时间')
    created_datetime = models.DateTimeField(auto_now_add=True)

    is_send = models.BooleanField(default=False, verbose_name='是否发布')

    def __str__(self):
        return self.title

    def get_params(self):
        return  model_to_dict(self)


