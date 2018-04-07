from django.conf.urls import url

from . import views
from weibos.apps.sina.models import ExaminationPointCategory

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^home/(?P<id>\d+)/$', views.home_page, name='home'),
    url(r'^home/list/$', views.home_page, name='home'),
    url(r'^examination/$', views.examination_page, {'obj': ExaminationPointCategory}, name='examination_page'),
]
