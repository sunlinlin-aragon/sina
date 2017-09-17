from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required(login_url='/admin/login/')
def index(request):

    return TemplateResponse(request, 'index.html', {'has_permission': True})
