# -*- coding:utf-8 -*-
import unittest
import mock

from ..tasks import ConcurrentAutomatchTask
from employee.models import EmployeeQuestionnaire
from employer.models import JobPosting
from employee import constants as employee_constants


class ConcurrentAutomatchTaskTestCase(unittest.TestCase):
    pass
#   @mock.patch('matches.tasks.Automatch.objects.create')
#   @mock.patch('matches.tasks.SearchQuerySet')
#   def test_run_should_create_automatch_for_each_job_posting_that_matches_a_questionnaire(
#           self, sqs_class, create):
#       # setup
#       task = ConcurrentAutomatchTask()
#       user = mock.Mock()
#       posting = JobPosting(
#           job_position=employee_constants.JOB_POSITION_CHOICES.JOB_POSITION_1,
#           schedule_type=employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME)
#       match = mock.Mock()
#       sqs = sqs_class.return_value.filter.return_value.models.return_value = \
#           [match]

#       # action
#       task.run(user, posting)

#       # assert
#       self.assertDictEqual(
#           dict(job_position__exact=posting.job_position,
#           schedule_type=posting.schedule_type),
#           sqs_class.return_value.filter.call_args[1])
#       self.assertTupleEqual((EmployeeQuestionnaire,),
#           sqs_class.return_value.filter.return_value.models.call_args[0])
#       self.assertDictEqual(
#           dict(user=user, match=match.object, source=posting),
#           create.call_args[1])

#   @mock.patch('matches.tasks.Automatch.objects.create')
#   @mock.patch('matches.tasks.SearchQuerySet')
#   def test_run_should_create_automatch_for_each_questionnaire_that_matches_a_job_posting(
#           self, sqs_class, create):
#       # setup
#       task = ConcurrentAutomatchTask()
#       user = mock.Mock()
#       questionnaire = EmployeeQuestionnaire(
#           job_position=employee_constants.JOB_POSITION_CHOICES.JOB_POSITION_1,
#           schedule_type=employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME)
#       match = mock.Mock()
#       sqs = sqs_class.return_value.filter.return_value.models.return_value = \
#           [match]

#       # action
#       task.run(user, questionnaire)

#       # assert
#       self.assertDictEqual(
#           dict(job_position__exact=questionnaire.job_position,
#           schedule_type=questionnaire.schedule_type),
#           sqs_class.return_value.filter.call_args[1])
#       self.assertTupleEqual((JobPosting,),
#           sqs_class.return_value.filter.return_value.models.call_args[0])
#       self.assertDictEqual(
#           dict(user=user, match=match.object, source=questionnaire),
#           create.call_args[1])
