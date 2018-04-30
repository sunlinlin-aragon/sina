# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse


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
        param = model_to_dict(self)
        param.pop('is_send', '')
        param.pop('send_datetime', '')
        param.pop('created_datetime', '')
        param.pop('id', '')
        param['cover'] = 'http://www.360ks.net' + param['cover'].url
        return param

    def get_admin_url(self):
        return '/admin/sina/article/%s/change/' % self.pk

    @staticmethod
    def add_url():
        return "/admin/sina/article/add/"


class Banner(models.Model):
    title = models.CharField(max_length=64, verbose_name='Banner 标题')
    banner_file = models.ImageField(upload_to='banner', verbose_name='图片地址', max_length=128)
    link = models.CharField(max_length=128, verbose_name='banner 链接')
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=True, verbose_name='是否发布')

    def __str__(self):
        return self.title

    def get_admin_url(self):
        return '/admin/sina/banner/%s/change/' % self.pk

    @staticmethod
    def add_url():
        return "/admin/sina/banner/add/"


class Category(models.Model):
    title = models.CharField(max_length=64, verbose_name='考试类别', unique=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_admin_url(self):
        return '/admin/sina/category/%s/change/' % self.pk

    @staticmethod
    def add_url():
        return "/admin/sina/category/add/"


level = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5'))


class ExaminationPointCategory(models.Model):
    title = models.CharField(max_length=64, verbose_name='考点类别名称', unique=True)
    level = models.CharField(choices=level, max_length=64, verbose_name='考点级别')
    category = models.ForeignKey(Category, verbose_name='考试类别')
    examination_point = models.ManyToManyField("self", verbose_name='考点类别', blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=True, verbose_name='是否发布')

    def __str__(self):
        '''
        这里影响前台的选择
        :return:
        '''
        return '%s--级别--%s--category--%s' % (self.title, self.level, self.category)

    def get_admin_url(self):
        return reverse('examination_point_category_update', kwargs={'pk': self.pk})

    @staticmethod
    def add_url():
        return reverse('examination_point_category_create')


class QuestionsManager(models.Manager):
    def get_queryset(self):
        return super(QuestionsManager, self).get_queryset()


class Questions(models.Model):
    title = models.CharField(max_length=512, verbose_name='问题标题')
    answer = models.CharField(max_length=16, verbose_name='问题答案')
    answer_description = models.CharField(max_length=1028, verbose_name='答案描述')
    category = models.ForeignKey(Category, verbose_name='考试类别')
    examination_point = models.ManyToManyField(ExaminationPointCategory, verbose_name='考点类别', blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=False, verbose_name='是否发布')
    look_num = models.BigIntegerField(verbose_name='浏览次数')

    objects = QuestionsManager()

    def __str__(self):
        return '%s' % self.title

    def get_admin_url(self):
        return reverse('questions_update', kwargs={'pk': self.pk})

    @staticmethod
    def add_url():
        return reverse('questions_create')

    def get_info(self):
        examination_point = self.examination_point.all().values('title')
        category = self.category.examinationpointcategory_set.all().values('title')
        return list(chain(examination_point, category))

    class Meta:
        ordering = ['-look_num', '-created_datetime']

    def get_related_point(self):
        return self.category.examinationpointcategory_set.all()


item_num_level = (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', "E"), ('F', 'F'), ('G', 'G'), ('H', 'H'))


class QuestionItems(models.Model):
    question = models.ForeignKey(Questions)
    item_num = models.CharField(choices=item_num_level, max_length=512, verbose_name='问题选项序号')
    item_des = models.TextField(max_length=512, verbose_name='问题选项描述')

    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("question", "item_num")
        ordering = ['item_num']