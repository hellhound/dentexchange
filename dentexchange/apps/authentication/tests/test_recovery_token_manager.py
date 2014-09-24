# -*- coding:utf-8 -*-
import unittest
import mock
import datetime

from django.utils.timezone import now

from ..models import RecoveryToken
from .. import constants


class RecoveryTokenManagerTestCase(unittest.TestCase):
    @mock.patch('authentication.models.models.Manager.get_queryset')
    @mock.patch('authentication.models.datetime')
    @mock.patch('authentication.models.now')
    def test_is_token_valid_should_return_true_when_valid_token(self,
            mocked_now, datetime_module, get_queryset):
        # setup
        manager = RecoveryToken.objects
        token = 'atoken'
        now_value = now()
        mocked_now.return_value = now_value
        datetime_module.timedelta = datetime.timedelta
        date_limit = now_value - datetime.timedelta(
            days=constants.RECOVERY_EXPIRATION_TIME_DAYS)
        get_queryset.return_value.filter.return_value.count.return_value = 1

        # action
        returned_value = manager.is_token_valid(token)

        # assert
        self.assertDictEqual(dict(token=token, timestamp__gte=date_limit),
            get_queryset.return_value.filter.call_args[1])
        self.assertTrue(returned_value)

    @mock.patch('authentication.models.models.Manager.get_queryset')
    @mock.patch('authentication.models.datetime')
    @mock.patch('authentication.models.now')
    def test_is_token_valid_should_return_false_when_invalid_token(self,
            mocked_now, datetime_module, get_queryset):
        # setup
        manager = RecoveryToken.objects
        token = 'atoken'
        now_value = now()
        mocked_now.return_value = now_value
        datetime_module.timedelta = datetime.timedelta
        date_limit = now_value - datetime.timedelta(
            days=constants.RECOVERY_EXPIRATION_TIME_DAYS)
        get_queryset.return_value.filter.return_value.count.return_value = 0

        # action
        returned_value = manager.is_token_valid(token)

        # assert
        self.assertDictEqual(dict(token=token, timestamp__gte=date_limit),
            get_queryset.return_value.filter.call_args[1])
        self.assertFalse(returned_value)
