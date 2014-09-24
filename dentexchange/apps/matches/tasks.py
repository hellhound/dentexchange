# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string as render_to_string_html
from django.template.loader import render_to_string as render_to_string_text
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from djcelery_transactions import PostTransactionTask as Task
from celery import chord, group

from haystack.query import SearchQuerySet, SQ

from registration.models import UserRegistration
from employee.models import EmployeeQuestionnaire
from employer.models import JobPosting
from .models import Automatch, Match
from . import strings, constants


class AutomatchTask(Task):
    def _get_user_registration(self, user):
        try:
            return user.userregistration
        except UserRegistration.DoesNotExist:
            return None

    def _get_job_postings(self, user):
        return JobPosting.objects.filter(
            praxis__business__user=user, is_posted=True
            ).prefetch_related('praxis')

    def _get_employee_questionnaire_as_list(self, user):
        try:
            return [user.employeequestionnaire]
        except EmployeeQuestionnaire.DoesNotExist:
            return []

    def _get_source_list(self, user):
        user_registration = self._get_user_registration(user)
        if user_registration is None:
            return []
        if user.userregistration.is_employer:
            return self._get_job_postings(user)
        return self._get_employee_questionnaire_as_list(user)

    def run(self, user=None, session_key=None):
        automatches = Automatch.objects.all()
        if user is not None:
            automatches = automatches.filter(user=user)
        automatches.delete()
        users = [user] if user is not None else User.objects.filter(
            userregistration__isnull=False)
        chord(
            (ConcurrentAutomatchTask().s(user, source)
            for user in users for source in self._get_source_list(user))
        )(JoinAutomatchTask().s(session_key=session_key))


class ConcurrentAutomatchTask(Task):
    def _is_employer(self, source_type):
        return source_type is JobPosting

    def _get_query(self, source):
        return dict(
            job_position__exact=source.job_position,
            schedule_type=source.schedule_type,
            visa=source.visa,
            state=source.praxis.state \
            if self._is_employer(type(source)) else source.state)
        return query

    def _get_sqs_model(self, source_type):
       return EmployeeQuestionnaire if self._is_employer(source_type) \
            else JobPosting

    def run(self, user, source):
        sqs = SearchQuerySet().filter(**self._get_query(source)
            ).models(self._get_sqs_model(type(source)))
        for match in sqs:
            # Sadly solr searches can return duplicate objects, so we need
            # to ensure that we are creating unique entries into the Automatch
            # table
            match = match.object
            # Recover the saved match
            try:
                saved_match = Match.objects.get(
                    match_content_type__model=type(match).__name__.lower(),
                    match_content_type__app_label=match._meta.app_label,
                    match_object_id=match.pk,
                    source_content_type__model=type(source).__name__.lower(),
                    source_content_type__app_label=source._meta.app_label,
                    source_object_id=source.pk)
            except Match.DoesNotExist:
                saved_match = None
            Automatch.objects.get_or_create(user=user,
                match_content_type__model=type(match).__name__.lower(),
                match_content_type__app_label=match._meta.app_label,
                match_object_id=match.pk,
                source_content_type__model=type(source).__name__.lower(),
                source_content_type__app_label=source._meta.app_label,
                source_object_id=source.pk,
                defaults=dict(user=user, match=match, source=source,
                saved_match=saved_match))


class JoinAutomatchTask(Task):
    def run(self, group_results, session_key=None):
        if session_key is not None:
            session = SessionStore(session_key=session_key)
            session[constants.REFRESH_AUTOMATCHES_TASK_DONE_SESSION_KEY] = True
            session.save()
            

class SendPeriodicAutomatchesEmailTask(Task):
    def run(self):
        group(ConcurrentSendPeriodicAutomatchesEmailTask().s(user)
            for user in User.objects.filter(userregistration__isnull=False))()


class ConcurrentSendPeriodicAutomatchesEmailTask(Task):
    def run(self, user):
        total_automatches = user.automatch_set.count()
        if total_automatches == 0:
            return
        html = render_to_string_html(
            'matches/mail/periodic_automatch_email.html',
            dict(user=user, total_automatches=total_automatches,
            http_host=settings.DOMAIN_NAME))
        body = render_to_string_text(
            'matches/mail/periodic_automatch_email.txt',
            dict(user=user, total_automatches=total_automatches,
            http_host=settings.DOMAIN_NAME))
        msg = EmailMultiAlternatives(
            strings.SEND_PERIODIC_AUTOMATCHES_EMAIL_SUBJECT % total_automatches,
            body, constants.FROM_PERIODIC_AUTOMATCHES_EMAIL, [user.email])
        msg.attach_alternative(html, 'text/html')
        msg.send()
