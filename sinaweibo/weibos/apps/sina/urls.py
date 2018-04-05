from django.conf.urls import url

from . import views
from .models import Article, Banner, Category, ExaminationPointCategory, Questions

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article_list/$', views.models_list, {'obj': Article}, name='inarticle_listdex'),
    url(r'^category_list/$', views.models_list, {'obj': Category}, name='category_list'),
    url(r'^examination_point_category_list/$', views.models_list, {'obj': ExaminationPointCategory}, name='examination_point_category_list'),
    url(r'^questions_list/$', views.models_list, {'obj': Questions}, name='questions_list'),
    url(r'^banner_list/$', views.models_list, {'obj': Banner}, name='banner_list'),
]
