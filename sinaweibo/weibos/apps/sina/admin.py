from django.contrib import admin

from weibos.apps.sina.models import Article, SinaApiData, Banner, Category, ExaminationPointCategory
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'cover', 'summary', 'text', 'send_datetime', 'is_send']
    list_display = ('title', 'send_datetime', 'is_send')


class BannerAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_per_page = 20
    list_display = ('title', 'created_datetime', 'is_send')


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_per_page = 20
    list_display = ('title', 'created_datetime')


class ExaminationPointCategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_per_page = 5
    list_display = ('title', 'level', 'category', 'created_datetime', 'is_send')

admin.site.register(Article, ArticleAdmin)
admin.site.register(SinaApiData)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(ExaminationPointCategory, ExaminationPointCategoryAdmin)