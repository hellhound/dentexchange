# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import Automatch


class AutomatchTestCase(unittest.TestCase):
    @mock.patch.object(Automatch, 'match')
    def test_unicode_should_return_get_job_position_display(self, match):
        # setup
        model = Automatch()
        job_position = 'Job Position'
        match.get_job_position_display.return_value = job_position

        # action
        returned_value = unicode(model)

        # assert
        self.assertEqual(job_position, returned_value)

    def test_get_email_should_return_email(self):
        # setup
        model = Automatch()
        model.user = User(email='an@example.com')

        # action
        email = model.get_email()

        # assert
        self.assertEqual(model.user.email, email)
