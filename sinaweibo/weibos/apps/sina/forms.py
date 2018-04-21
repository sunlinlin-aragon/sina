# -*- coding:utf-8 -*- 
# Author : sll
# @Time  : 2018/4/6 下午12:29

from django.forms import ModelForm
from .models import ExaminationPointCategory, Category, Questions, QuestionItems
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory


class ExaminationPointCategoryForm(ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='考试类别')

    class Meta:
        model = ExaminationPointCategory
        fields = ['title', 'level', 'category', 'examination_point', 'is_send']

    def clean(self):
        cleaned_data = self.cleaned_data
        level = cleaned_data.get('level')
        category = cleaned_data.get('category')
        examination_point = cleaned_data['examination_point']
        if level == '1':
            if not category:
                raise forms.ValidationError({'category': _('This field is required.')})
            else:
                cleaned_data['examination_point'] = []
            return cleaned_data
        else:
            if not examination_point:
                raise forms.ValidationError({'examination_point': _('This field is required.')})
            categorys = set([c.category.id for c in examination_point])
            if len(categorys) > 1:
                raise forms.ValidationError({'examination_point': _('考点类别部属于同一个category，请从新选择。')})
            cleaned_data['category'] = examination_point.first().category
        return cleaned_data

    def save(self, commit=True):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance


class QuestionsForm(ModelForm):
    title = forms.CharField(required=True, label='问题标题', widget=forms.Textarea(attrs={'rows': 2, 'cols': 80}))
    answer_description = forms.CharField(required=True, label='答案描述', widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}))

    class Meta:
        model = Questions
        fields = ['title', 'answer', 'answer_description', 'category', 'examination_point', 'is_send', 'look_num']

    def clean_examination_point(self):
        examination_point = self.cleaned_data['examination_point']
        categorys = set([c.category.id for c in examination_point])
        if len(categorys) > 1:
            raise forms.ValidationError('考点类别部属于同一个category，请从新选择。')
        return examination_point


class QuestionItemsForm(ModelForm):

    class Meta:
        model = QuestionItems
        fields = ['item_num', 'item_des']


QuestionsFormSet = inlineformset_factory(Questions, QuestionItems, fields=('item_num', 'item_des'), extra=8)


class BatchCreateQuestionsForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='考试类别')
    examination_point = forms.ModelMultipleChoiceField(queryset=ExaminationPointCategory.objects.all(), required=False, label='考点类别')
    file = forms.FileField(label='考题文件')

    def clean(self):
        cleaned_data = self.cleaned_data
        examination_point = cleaned_data['examination_point']
        categorys = set([c.category.id for c in examination_point])
        if len(categorys) > 1:
                raise forms.ValidationError({'examination_point': _('考点类别部属于同一个category，请从新选择。')})
        return cleaned_data