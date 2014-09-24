# -*- coding:utf-8 -*-
from employer.models import Praxis
from .models import Match


class PraxisFilterSerializer(object):
    def __init__(self, user):
        self._user = user

    def get_queryset(self):
        return Praxis.objects.filter(
            business__user=self._user, jobposting__isnull=False
            ).order_by('company_name', 'jobposting__position_name'
            ).values('pk', 'company_name', 'jobposting__pk',
            'jobposting__position_name')

    def serialize(self):
        queryset = self.get_queryset()
        praxes = []
        for raw_praxis in queryset:
            if len(praxes) == 0 or praxes[-1]['pk'] != raw_praxis['pk']:
                raw_praxis['job_postings'] = []
                praxes.append(raw_praxis)
            job_posting = dict(
                pk=raw_praxis.pop('jobposting__pk'),
                position_name=raw_praxis.pop('jobposting__position_name'))
            praxes[-1]['job_postings'].append(job_posting)
        return praxes


class AutomatchMatchManagementAdapter(object):
    class MatchAlreadyExistsException(Exception):
        pass

    class NoMatchException(Exception):
        pass

    def __init__(self, automatch):
        self.automatch = automatch

    def create(self):
        if self.automatch.saved_match is not None:
            raise self.MatchAlreadyExistsException()
        self.automatch.saved_match = Match.objects.create(
            user=self.automatch.user, match=self.automatch.match,
            source=self.automatch.source)
        self.automatch.save()

    def delete(self):
        if self.automatch.saved_match is None:
            raise self.NoMatchException()
        saved_match = self.automatch.saved_match
        self.automatch.saved_match = None
        self.automatch.save()
        saved_match.delete()
