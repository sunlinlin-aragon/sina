from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Article, ExaminationPointCategory, Questions
from .forms import ExaminationPointCategoryForm, QuestionsForm, QuestionsFormSet


@login_required(login_url='/admin/login/')
def index(request):
    return TemplateResponse(request, 'index.html')


@login_required(login_url='/admin/login/')
def models_list(request, obj):
    app_list = obj.objects.all()
    add_link = obj.add_url()
    return TemplateResponse(request, '%s_list.html' % obj._meta.model_name, {'has_permission': True, 'app_list': app_list, 'add_link': add_link, 'model_name': obj._meta.model_name})


@login_required(login_url='/admin/login/')
def create_examination_point_create(request):

    return TemplateResponse(request, 'examination_point_category_create.html',
                            {})


class ExaminationPointCategoryCreateOrUpdate(generic.UpdateView):

    template_name = 'examination_point_category_create.html'
    model = ExaminationPointCategory
    context_object_name = 'examinationpointcategory'
    form_class = ExaminationPointCategoryForm
    pk_url_kwarg = 'pk'
    success_url = '/dashboard/examination_point_category_list/'

    def get_object(self, queryset=None):
        self.creating = 'pk' not in self.kwargs
        self.pk = self.kwargs.get(self.pk_url_kwarg)
        if self.creating:
            return None
        else:
            obj = super(ExaminationPointCategoryCreateOrUpdate, self).get_object(queryset)
            return obj

    def get_context_data(self, **kwargs):
        ctx = super(ExaminationPointCategoryCreateOrUpdate, self).get_context_data(**kwargs)
        ctx['form'] = kwargs.get('form') or ExaminationPointCategoryForm(instance=self.object)
        return ctx

    def process_all_forms(self, form):
        if self.creating and form.is_valid():
            self.object = form.save()
        is_valid = form.is_valid()
        if is_valid:
            return self.forms_valid()
        else:
            return self.forms_invalid(form)

    form_valid = form_invalid = process_all_forms

    def forms_valid(self):
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form):
        if self.creating and self.object and self.object.pk is not None:
            self.object.delete()
            self.object = None
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        ctx = self.get_context_data(form=form)
        return self.render_to_response(ctx)


class QuestionsCreateUpdateView(generic.UpdateView):

    template_name = 'questions_create.html'
    model = Questions
    context_object_name = 'Questions'
    form_class = QuestionsForm
    questions_formset = QuestionsFormSet
    pk_url_kwarg = 'pk'
    success_url = '/dashboard/questions_list/'

    def __init__(self, *args, **kwargs):
        super(QuestionsCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets = {'questions_formset': self.questions_formset}

    def get_object(self, queryset=None):

        self.creating = 'pk' not in self.kwargs
        if self.creating:
            return None  # success
        else:
            obj = super(QuestionsCreateUpdateView, self).get_object(queryset)
            return obj

    def get_context_data(self, **kwargs):
        ctx = super(QuestionsCreateUpdateView, self).get_context_data(**kwargs)
        ctx['form'] = kwargs.get('form') or QuestionsForm(instance=self.object)
        for ctx_name, formset_class in self.formsets.items():
            if ctx_name not in ctx:
                ctx[ctx_name] = formset_class(instance=self.object)
        return ctx

    def get_form_kwargs(self):
        kwargs = super(QuestionsCreateUpdateView, self).get_form_kwargs()
        return kwargs

    def process_all_forms(self, form):
        if self.creating and form.is_valid():
            self.object = form.save()

        formsets = {}
        for ctx_name, formset_class in self.formsets.items():
            formsets[ctx_name] = formset_class(self.request.POST,
                                               instance=self.object)
        is_valid = form.is_valid() and all([formset.is_valid() for formset in formsets.values()])

        cross_form_validation_result = self.clean(form, formsets)
        if is_valid and cross_form_validation_result:
            return self.forms_valid(form, formsets)
        else:
            return self.forms_invalid(form, formsets)

    form_valid = form_invalid = process_all_forms

    def clean(self, form, formsets):
        return True

    def forms_valid(self, form, formsets):

        self.object = form.save()
        for formset in formsets.values():
            formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formsets):
        # delete the temporary product again
        if self.creating and self.object and self.object.pk is not None:
            self.object.delete()
            self.object = None

        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"))
        ctx = self.get_context_data(form=form, **formsets)
        return self.render_to_response(ctx)
