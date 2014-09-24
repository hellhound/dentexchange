# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import Business, Praxis


class PraxisTestCase(unittest.TestCase):
    def test_unicode_should_return_user_email(self):
        # setup
        model = Praxis()
        user = User(email='an@example.com')
        business = Business(user=user)
        model.business = business

        # action
        email = unicode(model)

        # assert
        self.assertEqual(model.business.user.email, email)

    def test_get_email_should_return_user_email(self):
        # setup
        model = Praxis()
        user = User(email='an@example.com')
        business = Business(user=user)
        model.business = business

        # action
        email = model.get_email()

        # assert
        self.assertEqual(model.business.user.email, email)
