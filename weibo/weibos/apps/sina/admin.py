from django.contrib import admin

from weibos.apps.sina.models import Article, SinaApiData
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'cover', 'summary', 'text', 'send_datetime', 'is_send']
    list_display = ('title', 'send_datetime', 'is_send')


admin.site.register(Article, ArticleAdmin)
admin.site.register(SinaApiData)