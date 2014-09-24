# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..models import RecoveryToken


class RecoveryTokenTestCase(unittest.TestCase):
    @mock.patch('authentication.models.models.Model.save')
    @mock.patch('authentication.models.uuid4')
    @mock.patch('authentication.models.hashlib')
    def test_save_should_assign_token_with_hash(self,
            hashlib_module, uuid4, save):
        # setup
        model = RecoveryToken()
        uuid4.return_value = 'uuid4'

        # action
        model.save()

        # assert
        self.assertEqual(1, uuid4.call_count)
        self.assertTupleEqual((uuid4.return_value,),
            hashlib_module.sha256.call_args[0])
        self.assertEqual(
            hashlib_module.sha256.return_value.hexdigest.return_value,
            model.token)
        self.assertEqual(1, save.call_count)

    def test_unicode_should_return_token(self):
        # setup
        model = RecoveryToken()
        token = 'atoken'
        model.token = token

        # action
        returned_value = unicode(model)

        # assert
        self.assertEqual(token, returned_value)

    def test_get_email_should_return_email(self):
        # setup
        model = RecoveryToken()
        model.user = User(email='an@example.com')

        # action
        email = model.get_email()

        # assert
        self.assertEqual(model.user.email, email)
