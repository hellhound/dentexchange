# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.http.response import Http404
from django import forms

from libs.mixins.views import (SuccessURLAliasViewMixin, HttpRefererViewMixin,
    KwargsUserFormViewMixin)
from libs import constants as lib_constants
from matches.models import Match
from .forms import EmployeeQuestionnaireForm, EmployeeQuestionnaireSignUpForm
from .models import EmployeeQuestionnaire
from . import strings, constants


class DashboardView(TemplateView):
    template_name = 'employee/dashboard.html'

    def get_context_data(self, **context):
        context = super(DashboardView, self).get_context_data(**context)
        context['matches'] = Match.objects.filter(user=self.request.user)
        return context


class AddEmployeeQuestionnaireFromSignUpFormView(SuccessURLAliasViewMixin,
        HttpRefererViewMixin, KwargsUserFormViewMixin, CreateView):
    template_name = 'employee/add_employee_questionnaire_form.html'
    success_url_alias = 'membership:home'
    form_class = EmployeeQuestionnaireSignUpForm
    initial = dict(
        schedule_type=constants.SCHEDULE_TYPE_CHOICES.PART_TIME, 
        compensation_type=constants.COMPENSATION_TYPE_CHOICES.HOURLY,
        visa=lib_constants.YES_NO_CHOICES.YES)

    def get_form_kwargs(self):
        kwargs = super(
            AddEmployeeQuestionnaireFromSignUpFormView, self).get_form_kwargs()
        kwargs.update(dict(skippable='_skip' in self.request.POST))
        return kwargs

    def form_invalid(self, form):
        temp_form = self.get_form(self.form_class)
        temp_form.is_valid()
        skippable = False
        try:
            temp_form.clean()
        except forms.ValidationError, error:
            if error.code == \
                    constants.QUESTIONNAIRE_FORM_INCOMPLETE_FORM_ERROR_CODE:
                skippable = True
        return self.render_to_response(
            self.get_context_data(skippable=skippable, form=form))


class AddEditEmployeeQuestionnaireFormViewMixin(SuccessURLAliasViewMixin,
        KwargsUserFormViewMixin):
    template_name = 'employee/add_edit_employee_questionnaire_form.html'
    success_url_alias = 'employee:dashboard'
    form_class = EmployeeQuestionnaireForm


class EditEmployeeQuestionnaireFromProfileFormView(
        AddEditEmployeeQuestionnaireFormViewMixin, UpdateView):
    model = EmployeeQuestionnaire


class AddEmployeeQuestionnaireFromProfileFormView(
        AddEditEmployeeQuestionnaireFormViewMixin, CreateView):
    initial = dict(
        schedule_type=constants.SCHEDULE_TYPE_CHOICES.PART_TIME, 
        compensation_type=constants.COMPENSATION_TYPE_CHOICES.HOURLY,
        visa=lib_constants.YES_NO_CHOICES.YES)


class PublicQuestionnaireDetailFromListView(DetailView):
    template_name = 'employee/public_questionnaire_detail_from_list.html'
    model = EmployeeQuestionnaire

    def get_object(self, queryset=None):
        pk = self.request.GET.get('pk')
        try:
            questionnaire = EmployeeQuestionnaire.objects.get(pk=pk)
        except EmployeeQuestionnaire.DoesNotExist:
            raise Http404
        return questionnaire
