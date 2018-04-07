from django.conf.urls import url

from . import views
from weibos.apps.sina.models import ExaminationPointCategory

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^home/(?P<id>\d+)/$', views.home_page, name='home'),
    url(r'^home/list/$', views.home_page, name='home'),
    url(r'^examination/(?P<id>\d+)/$', views.examination_list_page, name='examination_list_page'),
    url(r'^list_page/(?P<id>\d+)/$', views.list_page, name='list_page'),
    url(r'^question/(?P<id>\d+)/$', views.question_page, name='question_page'),
]
