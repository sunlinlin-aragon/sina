from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from .models import Article


@login_required(login_url='/admin/login/')
def index(request):

    app_list = Article.objects.all()
    return TemplateResponse(request, 'index.html', {'has_permission': True, 'app_list': app_list})
