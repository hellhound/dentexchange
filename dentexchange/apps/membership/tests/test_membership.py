# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import Membership


class MembershipTestCase(unittest.TestCase):
    def test_unicode_should_return_first_name_last_name(self):
        # setup
        model = Membership()
        model.first_name = 'First Name'
        model.last_name = 'Last Name'

        # action
        name = unicode(model)

        # assert
        self.assertEqual(name, u'%s %s' % (model.first_name, model.last_name))

    def test_get_email_should_return_email(self):
        # setup
        model = Membership()
        model.user = User(email='an@example.com')

        # action
        email = model.get_email()

        # assert
        self.assertEqual(model.user.email, email)
