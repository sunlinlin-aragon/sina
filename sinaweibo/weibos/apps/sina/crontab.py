from .models import Article, SinaApiData
import datetime
from sina_api import get_sina_weibo_access_token
import requests
from django.conf import settings


def send_sina_weibo(*args, **kwargs):
    try:
        sina_token = SinaApiData.objects.first().token
        send_articles = Article.objects.filter(send_datetime__gte = datetime.datetime.now() + datetime.timedelta(minutes=10), is_send = False)
        for article in send_articles:
            params = article.get_params()
            params['access_token'] = sina_token
            response = requests.post(settings.ARTICLE, data=params)
            article.is_send = True
            article.save(update_fields=['is_send'])
            print response
        print 'send success'
    except Exception, e:
        print str(e)