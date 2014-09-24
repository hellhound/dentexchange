# -*- coding:utf-8 -*-
import urllib

from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.db import models

from djcelery_transactions import PostTransactionTask as Task

from haystack.query import SearchQuerySet, SQ
from haystack.inputs import Clean

from libs import constants as libs_constants
from employer.models import Praxis, JobPosting
from employee.models import EmployeeQuestionnaire
from employee import strings as employee_strings
from employee import constants as employee_constants
from employer import strings as employer_strings
from .forms import SearchForm, SearchFiltersForm
from .import constants


class BaseSearchResultsTask(Task):
    def __init__(self):
        self._user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    def get_filtered_queryset(self, queryset, query):
        return queryset.filter(query)

    def join_search_queries(self, left, right):
        left = left if isinstance(left, SQ) else SQ(contains=Clean(left))
        right = right if isinstance(right, SQ) else SQ(contains=Clean(right))
        return left & right

    def reduce_query(self, keywords):
        query = reduce(self.join_search_queries, keywords)
        if not isinstance(query, SQ):
            return SQ(contains=Clean(query))
        return query

    def get_queryset(self, keywords, location, job_position=None,
            experience_years=None, distance=None, full_time=False,
            part_time=False, visa=False):
        sqs = SearchQuerySet().models(self.get_model()).all()
        if len(keywords) > 0:
            query = self.reduce_query(keywords)
            sqs = self.get_filtered_queryset(sqs, query)
        if location != '':
            sqs = self.get_filtered_queryset(sqs,
                self.get_query_by_location(location))
        if job_position not in (None, ''):
            sqs = self.get_filtered_queryset(sqs,
                SQ(job_position=job_position))
        if experience_years not in (None, ''):
            sqs = self.get_filtered_queryset(sqs,
                SQ(experience_years=experience_years))
        if full_time:
            sqs = self.get_filtered_queryset(sqs,SQ(schedule_type=\
                employee_constants.SCHEDULE_TYPE_CHOICES.FULL_TIME))
        if part_time:
            sqs = self.get_filtered_queryset(sqs,SQ(schedule_type=\
                employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME))
        if visa:
            sqs = self.get_filtered_queryset(sqs, SQ(visa=True))
        return sqs

    def get_object_list(self, queryset):
        object_list = []
        if len(queryset) > 0:
            user = self.user
            best_match = queryset.best_match()
            for obj in (r for r in queryset if r is not None):
                if obj.matches is None:
                    was_saved = False
                else:
                    matches = filter(lambda x: x == str(user.pk), obj.matches)
                    was_saved = len(matches) > 0
                object_list.append(self.get_object(obj, best_match, was_saved))
        return object_list

    def get_model(self):
        raise NotImplementedError(u'get_model() should be implemented')

    def get_query_by_location(self, location):
        raise NotImplementedError(
            u'get_query_by_location() should be implemented')

    def get_object(self, obj, best_match, was_saved):
        raise NotImplementedError(u'get_object() should be implemented')

    def run(self, data, user, session_key):
        search_form = SearchForm(data=data)
        filters_form = SearchFiltersForm(data=data)
        search_form.is_valid()
        filters_form.is_valid()
        keywords = search_form.cleaned_data.get(
            'keywords', '').lower().strip().split()
        location = search_form.cleaned_data.get(
            'location', '').lower().strip()
        job_position = filters_form.cleaned_data.get('job_position')
        experience_years = filters_form.cleaned_data.get('experience_years')
        distance = filters_form.cleaned_data.get('distance')
        full_time = filters_form.cleaned_data.get('full_time', False)
        part_time = filters_form.cleaned_data.get('part_time', False)
        visa = filters_form.cleaned_data.get('visa', False)
        was_search_button_clicked = data.get('_search', '0') == '1'
        self.user = user
        results = dict(results=[])
        if len(keywords) > 0 or location != '' or was_search_button_clicked:
            queryset = self.get_queryset(keywords, location, job_position,
                experience_years, distance, full_time, part_time, visa)
            object_list = self.get_object_list(queryset)
            results['results'] = dict(object_list=object_list)
        session = SessionStore(session_key=session_key)
        session[constants.RESULTS_BEACON_TASK_DONE_SESSION_KEY] = results
        session.save()


class EmployeeSearchResultsTask(BaseSearchResultsTask):
    contact_template = 'contact/mail/employee_contact_body.txt'

    def get_model(self):
        return JobPosting

    def get_query_by_location(self, location):
        return SQ(address=location) | SQ(zip_code=location) \
            | SQ(city=location) | SQ(state=location)

    def get_object(self, obj, best_match, was_saved):
        contact_email_body = urllib.quote(render_to_string(
            self.contact_template,
            dict(http_host=settings.DOMAIN_NAME, pk=obj.pk,
            user=self.user, company_name=obj.company_name)))
        return dict(
            pk=obj.pk,
            contact_email=obj.email,
            contact_email_subject=unicode(
                employee_strings.EMPLOYEE_CONTACT_SUBJECT),
            contact_email_body=contact_email_body,
            posting_title=obj.posting_title,
            schedule_type=obj.schedule_type_text,
            wage=obj.annualy_wage_text if obj.compensation_type \
                else obj.hourly_wage_text,
            job_position=obj.job_position_text,
            address=obj.address,
            state=obj.state,
            percentage=100. * obj.score / best_match.score,
            score=obj.score,
            was_saved=was_saved)


class EmployerSearchResultsTask(BaseSearchResultsTask):
    contact_template = 'contact/mail/employer_contact_body.txt'

    def get_model(self):
        return EmployeeQuestionnaire

    def get_query_by_location(self, location):
        return  SQ(zip_code=location) | SQ(city=location) \
            | SQ(state=location)

    def get_object(self, obj, best_match, was_saved):
        contact_email_body = urllib.quote(render_to_string(
            self.contact_template,
            dict(http_host=settings.DOMAIN_NAME, pk=obj.pk,
            first_name=obj.first_name, last_name=obj.last_name)))
        return dict(
            pk=obj.pk,
            contact_email=obj.email,
            contact_email_subject=unicode(
                employer_strings.EMPLOYER_CONTACT_SUBJECT),
            contact_email_body=contact_email_body,
            schedule_type=obj.schedule_type_text,
            wage=obj.annualy_wage_text if obj.compensation_type \
                else obj.hourly_wage_text,
            job_position=obj.job_position_text,
            city=obj.city,
            state=obj.state,
            distance=obj.distance_text,
            percentage=100. * obj.score / best_match.score,
            score=obj.score,
            was_saved=was_saved)
