# -*- coding:utf-8 -*-
import json

from django.views.generic.base import View
from django.http import Http404

from braces import views

from libs.views.list import DentexchangeListView
from employee.models import EmployeeQuestionnaire
from employer.models import JobPosting
from .utils import PraxisFilterSerializer, AutomatchMatchManagementAdapter
from .models import Match, Automatch
from .tasks import AutomatchTask
from . import constants


class ActionMatchViewMixin(object):
    def get_ajax(self, request, *args, **kwargs):
        pk = request.GET.get('pk')
        try:
            matching_object = self.model.objects.get(pk=pk)
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            # Bad Request
            return self.render_json_response(dict(status='error'), status=400)
        try:
            extra_context = self.action_over_matching_object(matching_object)
        except Http404:
            # Bad Request
            return self.render_json_response(dict(status='error'), status=400)
        context = dict(status='ok')
        context.update(extra_context)
        return self.render_json_response(context)

    def action_over_matching_object(self, matching_object):
        raise NotImplementedError(
            'Should implement action_over_matching_object()')


class AddMatchViewMixin(ActionMatchViewMixin):
    def action_over_matching_object(self, matching_object):
        Match.objects.create(user=self.request.user, match=matching_object)
        return {}


class AddJobPostingMatchView(AddMatchViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = JobPosting


class AddQuestionnaireMatchView(AddMatchViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = EmployeeQuestionnaire


class DeleteMatchViewMixin(ActionMatchViewMixin):
    def action_over_matching_object(self, matching_object):
        try:
            match = matching_object.matches.get(user=self.request.user)
        except Match.DoesNotExist:
            raise Http404
        match.delete()
        return dict(total=self.request.user.match_set.count())


class DeleteJobPostingMatchView(DeleteMatchViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = JobPosting


class DeleteQuestionnaireMatchView(DeleteMatchViewMixin,
        views.JSONResponseMixin, views.AjaxResponseMixin, View):
    model = EmployeeQuestionnaire


class AddFromAutomatchView(ActionMatchViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = Automatch

    def action_over_matching_object(self, automatch):
        try:
            AutomatchMatchManagementAdapter(automatch).create()
        except AutomatchMatchManagementAdapter.MatchAlreadyExistsException:
            pass
        return {}


class DeleteFromAutomatchView(ActionMatchViewMixin, views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    model = Automatch

    def action_over_matching_object(self, automatch):
        try:
            AutomatchMatchManagementAdapter(automatch).delete()
        except AutomatchMatchManagementAdapter.NoMatchException:
            pass
        return {}


class SavedMatchesViewMixin(object):
    def get_queryset(self):
        return self.request.user.match_set.all()


class QuestionnaireSavedMatchesView(SavedMatchesViewMixin,
        DentexchangeListView):
    template_name = 'matches/questionnaire_saved_matches.html'


class JobPostingSavedMatchesView(SavedMatchesViewMixin, DentexchangeListView):
    template_name = 'matches/posting_saved_matches.html'


class BaseAutomatchesView(DentexchangeListView):
    def get_queryset(self):
        return Automatch.objects.filter(user=self.request.user)


class JobPostingAutomatchesView(BaseAutomatchesView):
    template_name = 'matches/posting_automatches.html'


class QuestionnaireAutomatchesView(BaseAutomatchesView):
    template_name = 'matches/questionnaire_automatches.html'

    def get_filters(self):
        filters = {}
        praxis_pk = self.request.GET.get('praxis_pk', '').strip()
        job_posting_pk = self.request.GET.get('job_posting_pk', '').strip()
        try:
            if praxis_pk != '':
                filters['praxis__pk'] = int(praxis_pk)
            if job_posting_pk != '':
                filters['pk'] = int(job_posting_pk)
        except ValueError:
            raise HttpError
        job_posting_pks = JobPosting.objects.values_list('pk').filter(**filters)
        return dict(source_content_type__name__iexact='job posting',
            source_object_id__in=job_posting_pks)

    def get_queryset(self):
        return super(QuestionnaireAutomatchesView, self).get_queryset().filter(
            **self.get_filters())

    def get_context_data(self, **context):
        context = super(QuestionnaireAutomatchesView, self
            ).get_context_data(**context)
        context['praxes'] = json.dumps(PraxisFilterSerializer(
            self.request.user).serialize())
        return context


class RefreshAutomatchView(views.JSONResponseMixin, views.AjaxResponseMixin,
        View):
    def get_ajax(self, request, *args, **kwargs):
        AutomatchTask().delay(
            user=self.request.user, session_key=request.session.session_key)
        return self.render_json_response(dict(status='ok'))


class RefreshAutomatchBeaconView(views.JSONResponseMixin,
        views.AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        if request.session.get(
                constants.REFRESH_AUTOMATCHES_TASK_DONE_SESSION_KEY, False):
            request.session.pop(
                constants.REFRESH_AUTOMATCHES_TASK_DONE_SESSION_KEY)
            return self.render_json_response(dict(done=True))
        return self.render_json_response(dict(done=False))
