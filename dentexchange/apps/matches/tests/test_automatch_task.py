# -*- coding:utf-8 -*-
import unittest
import mock

from ..tasks import AutomatchTask
from registration.models import UserRegistration
from employee.models import EmployeeQuestionnaire


class AutomatchTaskTestCase(unittest.TestCase):
    pass
#   @mock.patch('matches.tasks.User.objects.filter')
#   @mock.patch('matches.tasks.Automatch.objects.all')
#   def test_run_should_erase_all_automatches(
#           self, automatch_all, user_filter):
#       # setup
#       task = AutomatchTask()
#       user_filter.return_value = []

#       # action
#       task.run()

#       # assert
#       self.assertEqual(1, automatch_all.return_value.delete.call_count)

#   @mock.patch('matches.tasks.ConcurrentAutomatchTask.delay')
#   @mock.patch('matches.tasks.JobPosting.objects.filter')
#   @mock.patch('matches.tasks.User.objects.filter')
#   @mock.patch('matches.tasks.Automatch.objects.all')
#   def test_run_should_call_concurrent_automatch_tasks_delay_with_user_and_source_for_each_user_and_each_source_when_the_user_is_employer(
#           self, automatch_all, user_filter, job_posting_filter, delay):
#       # setup
#       task = AutomatchTask()
#       user = mock.Mock()
#       user.userregistration.is_employer = True
#       user_filter.return_value = [user]
#       posting = mock.Mock()
#       job_posting_filter.return_value = [posting]

#       # action
#       task.run()

#       # assert
#       self.assertDictEqual(dict(userregistration__isnull=False),
#           user_filter.call_args[1])
#       self.assertDictEqual(dict(praxis__business__user=user, is_posted=True),
#           job_posting_filter.call_args[1])
#       self.assertTupleEqual((user, posting,), delay.call_args[0])

#   @mock.patch('matches.tasks.ConcurrentAutomatchTask.delay')
#   @mock.patch('matches.tasks.JobPosting.objects.filter')
#   @mock.patch('matches.tasks.User.objects.filter')
#   @mock.patch('matches.tasks.Automatch.objects.all')
#   def test_run_should_call_concurrent_automatch_tasks_delay_with_user_and_source_for_each_user_and_each_source_when_the_user_is_employee(
#           self, automatch_all, user_filter, job_posting_filter, delay):
#       # setup
#       task = AutomatchTask()
#       questionnaire = mock.Mock()
#       user = mock.Mock()
#       user.employeequestionnaire = questionnaire
#       user.userregistration.is_employer = False
#       user_filter.return_value = [user]

#       # action
#       task.run()

#       # assert
#       self.assertDictEqual(dict(userregistration__isnull=False),
#           user_filter.call_args[1])
#       self.assertTupleEqual((user, questionnaire,), delay.call_args[0])

#   @mock.patch('matches.tasks.ConcurrentAutomatchTask.delay')
#   @mock.patch('matches.tasks.User.objects.filter')
#   @mock.patch('matches.tasks.Automatch.objects.all')
#   def test_run_shouldnt_call_concurrent_automatch_tasks_delay_if_the_user_doesnt_have_a_questionnaire(
#           self, automatch_all, user_filter, delay):
#       # setup
#       task = AutomatchTask()
#       class UserMock(mock.Mock):
#           @property
#           def employeequestionnaire(self):
#               raise EmployeeQuestionnaire.DoesNotExist()
#       user = UserMock()
#       user.userregistration.is_employer = False
#       user_filter.return_value = [user]

#       # action
#       task.run()

#       # assert
#       self.assertEqual(0, delay.call_count)

#   @mock.patch('matches.tasks.ConcurrentAutomatchTask.delay')
#   @mock.patch('matches.tasks.User.objects.filter')
#   @mock.patch('matches.tasks.Automatch.objects.all')
#   def test_run_shouldnt_call_concurrent_automatch_tasks_delay_if_the_user_doesnt_have_a_user_registration(
#           self, automatch_all, user_filter, delay):
#       # setup
#       task = AutomatchTask()
#       class UserMock(mock.Mock):
#           @property
#           def userregistration(self):
#               raise UserRegistration.DoesNotExist()
#       user = UserMock()
#       user_filter.return_value = [user]

#       # action
#       task.run()

#       # assert
#       self.assertEqual(0, delay.call_count)
