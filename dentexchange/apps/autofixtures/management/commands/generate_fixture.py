# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand

from ...builders import EmployerBuilder, EmployeeBuilder
from ... import constants

class Command(BaseCommand):
    help = '''
        Generates %i random employers and %i random employees. Each employer
        can have %i to %i job postings. The whole site will have a total of %i
        job postings.
    ''' % (constants.TOTAL_EMPLOYERS, constants.TOTAL_EMPLOYEES,
        constants.POSTINGS_PER_EMPLOYER_MIN,
        constants.POSTINGS_PER_EMPLOYER_MAX, constants.TOTAL_POSTINGS)

    def handle(self, *args, **options):
        [EmployerBuilder().build() for _ in xrange(constants.TOTAL_EMPLOYERS)]
        [EmployeeBuilder().build() for _ in xrange(constants.TOTAL_EMPLOYEES)]
