from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from weibos.apps.sina.models import Article, Banner, Category, Questions, ExaminationPointCategory
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin/login/')
def home_page(request, id=1):
    if request.is_ajax():
        id = request.GET.get('id') or 1
    questions = Questions.objects.filter(category_id=id).order_by('-look_num').values('id', 'title', 'look_num')
    paginator = Paginator(questions, 10)
    category = Category.objects.filter(id=id).first()
    if request.is_ajax():
        page = request.GET.get('page')
        json_context = paginator.page(page)
        return JsonResponse({'questions': list(json_context.object_list)})
    else:    
        template = 'home.html'
        banner_info = Banner.objects.all()[:5]
        menu_info = Category.objects.all()
        questions_list = paginator.page(1)
        page_range = paginator.num_pages
        meta_title = Category.objects.filter(id=id).first()
        context = {
            'banner_info': banner_info,
            'menu_info': menu_info,
            'questions': questions_list,
            'active_id': int(id),
            'page_number': 1,
            'page_range': page_range,
            'meta_title': meta_title.title if meta_title else '',
            'category': category.title if category else ''
        }
        return TemplateResponse(request, template, context)


@login_required(login_url='/admin/login/')
def examination_list_page(request, id):
    template = 'examination_page.html'
    category_list = Category.objects.all()
    examination_point = ExaminationPointCategory.objects.filter(category_id=id).values('id', 'title')
    meta_title = Category.objects.filter(id=id).first()
    context = {
        'category_list': category_list,
        'active_id': int(id),
        'examination_point': examination_point,
        'meta_title': meta_title.title if meta_title else '',
    }
    return TemplateResponse(request, template, context)


@login_required(login_url='/admin/login/')
def list_page(request, id=1):
    template = 'list.html'
    if request.is_ajax():
        id = request.GET.get('id') or 1
    examination_point = ExaminationPointCategory.objects.filter(id=id).first()
    questions = examination_point.questions_set.all().order_by('-look_num').values('id', 'title', 'look_num')
    paginator = Paginator(questions, 10)
    if request.is_ajax():
        page = request.GET.get('page')
        json_context = paginator.page(page)
        return JsonResponse({'questions': list(json_context.object_list)})
    else:
        page_range = paginator.num_pages
        questions_list = paginator.page(1)
        meta_title = ExaminationPointCategory.objects.filter(id=id).first()
        context = {
            'examination_point': examination_point,
            'active_id': int(id),
            'questions': questions_list,
            'page_number': 1,
            'page_range': page_range,
            'meta_title': meta_title.title if meta_title else '',
        }
        return TemplateResponse(request, template, context)


@login_required(login_url='/admin/login/')
def question_page(request, id):
    template = 'question_info.html'
    question_info = Questions.objects.filter(id=id).first()
    question_item = question_info.questionitems_set.all()
    context = {
        'question_info': question_info,
        'question_item': question_item,
    }
    return TemplateResponse(request, template, context)