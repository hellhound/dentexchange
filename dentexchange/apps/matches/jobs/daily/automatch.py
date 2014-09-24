# -*- coding:utf-8 -*-
from django_extensions.management.jobs import DailyJob

from ...tasks import AutomatchTask


class Job(DailyJob):
    help = '''
    Gets matching job postings for employees and questionnaires for 
    employers based on a given criteria and stores these matches on
    matches.Automatch
    '''

    def execute(self):
        AutomatchTask.delay()
