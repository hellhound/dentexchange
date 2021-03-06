# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import Business


class BusinessTestCase(unittest.TestCase):
    def test_unicode_should_return_user_email(self):
        # setup
        model = Business()
        model.user = User(email='an@example.com')

        # action
        email = unicode(model)

        # assert
        self.assertEqual(model.user.email, email)

    def test_get_email_should_return_email(self):
        # setup
        model = Business()
        model.user = User(email='an@example.com')

        # action
        email = model.get_email()

        # assert
        self.assertEqual(model.user.email, email)
