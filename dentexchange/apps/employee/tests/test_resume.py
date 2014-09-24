# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import Resume


class ResumeTestCase(unittest.TestCase):
    def test_unicode_should_return_email(self):
        # setup
        model = Resume()
        model.user = User(email='an@example.com')

        # action
        email = unicode(model)

        # assert
        self.assertEqual(model.user.email, email)

    def test_get_email_should_return_email(self):
        # setup
        model = Resume()
        model.user = User(email='an@example.com')

        # aqction
        email = model.get_email()

        # assert
        self.assertEqual(model.user.email, email)
