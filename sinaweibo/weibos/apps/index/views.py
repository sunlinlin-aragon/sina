from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from weibos.apps.sina.models import Article, Banner, Category, Questions, ExaminationPointCategory


def home_page(request, id=1):
    questions = Questions.objects.filter(category_id=id).values('id', 'title', 'look_num')
    paginator = Paginator(questions, 10)
    if request.is_ajax():
        page = request.GET.get('page')
        json_context = paginator.page(page)
        return JsonResponse(json_context)
    else:    
        template = 'home.html'
        banner_info = Banner.objects.all()[:5]
        menu_info = Category.objects.all()
        questions_list = paginator.page(1)
        context = {
            'banner_info': banner_info,
            'menu_info': menu_info,
            'questions': questions_list,
            'active_id': id,
        }
        return TemplateResponse(request, template, context)


def examination_page(request, obj):
    template = 'examination_page.html'
    examination_point_category = obj.objects.all()
    context = {
    }
    return TemplateResponse(request, template, context)