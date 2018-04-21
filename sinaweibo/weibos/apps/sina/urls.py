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
    url(r'^examination_point_category/create/$', views.ExaminationPointCategoryCreateOrUpdate.as_view(), name='examination_point_category_create'),
    url(r'^examination_point_category/(?P<pk>\d+)/update/$', views.ExaminationPointCategoryCreateOrUpdate.as_view(), name='examination_point_category_update'),
    url(r'^questions/create/$', views.QuestionsCreateUpdateView.as_view(), name='questions_create'),
    url(r'^questions/(?P<pk>\d+)/update/$', views.QuestionsCreateUpdateView.as_view(), name='questions_update'),
    url(r'^batch_create_questions/$', views.BatchCreateQuestionsView.as_view(), name='batch-create-questions'),
    url(r'^preview-file-questions/$', views.BatchCreateQuestionsView.as_view(), name='preview-file-questions'),

]
