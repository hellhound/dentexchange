# -*- coding:utf-8 -*-
import unittest
import mock

from ..jobs.daily.automatch import Job


class AutomatchJobTestCase(unittest.TestCase):
    @mock.patch('matches.jobs.daily.automatch.AutomatchTask.delay')
    def test_execute_should_call_automatch_tasks_delay(self, delay):
        # setup
        job = Job()

        # action
        job.execute()

        # assert
        self.assertEqual(1, delay.call_count)
