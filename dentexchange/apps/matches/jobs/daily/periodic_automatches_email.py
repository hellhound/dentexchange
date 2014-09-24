# -*- coding:utf-8 -*-
import calendar

from django_extensions.management.jobs import DailyJob
from django.utils.timezone import now

from ...tasks import SendPeriodicAutomatchesEmailTask
from ... import constants


class Job(DailyJob):
    help = '''
    Sends periodic email notifications to users notifying the total automatches
    they have in their profiles
    '''

    def execute(self):
        today = now()
        week_day = calendar.weekday(today.year, today.month, today.day)
        if week_day in constants.PERIODIC_AUTOMATCHES_PROGRAMMED_WEEK_DAYS:
            SendPeriodicAutomatchesEmailTask.delay()
