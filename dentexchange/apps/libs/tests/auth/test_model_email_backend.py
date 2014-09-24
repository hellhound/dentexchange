# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.exceptions import ObjectDoesNotExist

from ...auth.backends import ModelEmailBackend


class ModelEmailBackendTestCase(unittest.TestCase):
    def setUp(self):
        self.username = 'username'
        self.password = 'password'

    @mock.patch('libs.auth.backends.get_user_model')
    def test_authenticate_should_return_user_when_email_password_ok(self,
            get_user_model):
        # setup
        backend = ModelEmailBackend()
        user = mock.Mock()
        user_model = get_user_model.return_value
        user_model.objects.get = mock.Mock(return_value=user)
        user.check_password = mock.Mock(return_value=True)

        # action
        returned_user = backend.authenticate(username=self.username,
            password=self.password)

        # assert
        self.assertDictEqual(dict(email=self.username),
            user_model.objects.get.call_args[1])
        self.assertEqual(self.password, user.check_password.call_args[0][0])
        self.assertEqual(id(user), id(returned_user))

    @mock.patch('libs.auth.backends.get_user_model')
    def test_authenticate_should_return_none_when_password_not_ok(self,
            get_user_model):
        # setup
        backend = ModelEmailBackend()
        user = mock.Mock()
        user_model = get_user_model.return_value
        user_model.objects.get = mock.Mock(return_value=user)
        user.check_password = mock.Mock(return_value=False)

        # action
        returned_user = backend.authenticate(username=self.username,
            password=self.password)

        # assert
        self.assertEqual(None, returned_user)

    @mock.patch('libs.auth.backends.get_user_model')
    def test_authenticate_should_return_none_when_user_doesnt_exist(self,
            get_user_model):
        # setup
        backend = ModelEmailBackend()
        user = mock.Mock()
        user_model = get_user_model.return_value
        user_model.configure_mock(DoesNotExist=ObjectDoesNotExist)
        user_model.objects.get = mock.Mock(
            side_effect=user_model.DoesNotExist())

        # action
        returned_user = backend.authenticate(username=self.username,
            password=self.password)

        # asert
        self.assertEqual(None, returned_user)
