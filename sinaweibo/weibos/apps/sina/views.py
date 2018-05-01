# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from .models import Article, ExaminationPointCategory, Questions, QuestionItems
from .forms import ExaminationPointCategoryForm, QuestionsForm, QuestionsFormSet, BatchCreateQuestionsForm
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, sys
import random


reload(sys)
sys.setdefaultencoding('utf-8')

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
        if self.creating:
            if ExaminationPointCategory.objects.filter(title=form.data['title']).exists():
                form.errors.update({'title': ['%s 已经存在'% form.data['title']]})
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


ITEM_NUM_MAPPING = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K'}
class BatchCreateQuestionsView(FormView):
    form_class = BatchCreateQuestionsForm
    template_name = 'batch_create_questions.html'  # Replace with your template.
    success_url = '/dashboard/batch_create_questions/'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            file_s = request.FILES['file']
            question_list = self.handle_uploaded_file(file_s)
            return JsonResponse({'content': question_list})
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            if form.is_valid():
                file_s = request.FILES['file']
                data = form.cleaned_data
                question_list = self.handle_uploaded_file(file_s)
                sync_info = self.save_info(data, question_list)
                messages.info(self.request, _("问题添加成功, "))
                ctx = self.get_context_data(form=form)
                ctx.update(sync_info)
                return self.render_to_response(ctx)
            else:
                return self.form_invalid(form)

    def handle_uploaded_file(self, f):
        # with open(os.path.join(settings.BASE_DIR, 'weibos/media/questions/name.txt'), 'wb+') as destination:
        items_line= []
        index_split = [0]
        all_lines = f.readlines()
        new_all_line = [line.decode('gbk') for line in all_lines]
        for index, line in enumerate(new_all_line):
            if line == '\r\n':
                index_split.append(index)
        index_split.append(-1)
        if index_split:
            for index, _ in enumerate(index_split):
                if _ == -1:
                    break
                start, end = index_split[index] + 1, index_split[index + 1]
                if index == 0:
                    start = 0
                items_line.append(new_all_line[start: end])
        return self.handle_questions(items_line)

    def handle_questions(self, items):
        question_list = []
        for item in items:
            question = {}
            question_items = []
            for i in item:
                if i.split('.')[0].isdigit():
                    question['title'] = i
                if 'title' in question and not i.startswith('答案') and not i.startswith('试题解析') and not i.split('.')[0].isdigit():
                    question_items.append(i)
                if i.startswith('答案'):
                    question['answer'] = i
                if i.startswith('试题解析'):
                    question['answer_description'] = i
            if not question_items:
                continue
            question['question_items'] = question_items
            question_list.append(question)
        return question_list

    def save_info(self, data, question_list):
        category = data.get('category')
        examination_point = data.get('examination_point')
        fail_num = 0
        success_item = []
        exists_item = []
        for question in question_list:
            title = question.get('title')
            answer = question.get('answer')
            answer_description = question.get('answer_description')
            question_items = question.get('question_items')

            if title and answer and question_items:
                if Questions.objects.filter(title=title.split('.', 1)[-1]).exists():
                    exists_item.append(title.split('.')[0])
                    continue
                new_question = Questions()
                new_question.category = category
                new_question.title = title.split('.', 1)[-1]
                new_question.answer = answer.split(':')[-1]
                new_question.answer_description = answer_description.split(':')[-1] if answer_description else ''
                new_question.look_num = random.randint(0, 10)
                new_question.save()
                for point in examination_point:
                    new_question.examination_point.add(point)
                new_question.save()

                for index, item in enumerate(question_items):
                    new_questionitem = QuestionItems()
                    new_questionitem.question = new_question
                    new_questionitem.item_num = ITEM_NUM_MAPPING.get(index)
                    new_questionitem.item_des = item
                    new_questionitem.save()
                success_item.append(title.split('.')[0])
            else:
                fail_num += 1

        return {'success_item': success_item, "exists_item": exists_item, "fail_num": fail_num}


def save_question(request):
    ids = request.POST.get('values')
    if ids:
        ids = ids.split(',')
        Questions.objects.filter(id__in=ids).update(is_send=True)
        return JsonResponse({'success': True})