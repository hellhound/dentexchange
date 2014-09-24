# -*- coding:utf-8 -*-
from django.views.generic.base import TemplateView, View
from django.views.generic.list import MultipleObjectMixin

from braces import views

from .tasks import EmployeeSearchResultsTask, EmployerSearchResultsTask
from .forms import SearchForm, SearchFiltersForm
from . import constants


class SearchViewMixin(object):
    def get_context_data(self, **context):
        context = super(SearchViewMixin, self).get_context_data(**context)
        context['form'] = SearchForm()
        context['filters_form'] = SearchFiltersForm()
        context['base_template'] = self.base_template
        return context


class EmployeeSearchView(SearchViewMixin, TemplateView):
    template_name = 'search/employee_search_view.html'
    base_template = 'employee/base.html'


class EmployerSearchView(SearchViewMixin, TemplateView):
    template_name = 'search/employer_search_view.html'
    base_template = 'employer/base.html'


class BaseResultsView(MultipleObjectMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    def get_paginate_by(self, queryset):
        return libs_constants.PAGINATE_BY

    def get_ajax(self, request, *args, **kwargs):
        self.task().delay(
            request.GET, request.user, request.session.session_key)
        return self.render_json_response(dict(status='ok'))


class EmployeeResultsView(BaseResultsView):
    task = EmployeeSearchResultsTask


class EmployerResultsView(BaseResultsView):
    task = EmployerSearchResultsTask


class ResultsBeaconView(views.JSONResponseMixin, views.AjaxResponseMixin,
        View):
    def get_ajax(self, request, *args, **kwargs):
        if request.session.has_key(
                constants.RESULTS_BEACON_TASK_DONE_SESSION_KEY):
            results = request.session.pop(
                constants.RESULTS_BEACON_TASK_DONE_SESSION_KEY)
            results.update(dict(done=True))
            return self.render_json_response(results)
        return self.render_json_response(dict(done=False))
