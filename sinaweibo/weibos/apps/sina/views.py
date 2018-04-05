from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from .models import Article


@login_required(login_url='/admin/login/')
def index(request):
    return TemplateResponse(request, 'index.html')


@login_required(login_url='/admin/login/')
def models_list(request, obj):
    app_list = obj.objects.all()
    add_link = obj.add_url()
    return TemplateResponse(request, '%s_list.html' % obj._meta.model_name, {'has_permission': True, 'app_list': app_list, 'add_link': add_link, 'model_name': obj._meta.model_name})
