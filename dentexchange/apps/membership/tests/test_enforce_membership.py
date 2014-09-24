# -*- coding:utf-8 -*-
import unittest
import mock
import datetime

from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now as django_now, utc

from ..decorators import enforce_membership
from ..models import Membership
from .. import constants


class EnforceMembershipTestCase(unittest.TestCase):
    def setUp(self):
        self.args = (1, 2, 3,)
        self.kwargs = dict(one=1, two=2, three=3)

    @mock.patch('membership.decorators.now')
    def test_enforce_membership_should_execute_and_return_view(self, now):
        # setup
        view = mock.Mock(return_value=mock.MagicMock())
        wrapped_view = enforce_membership(view)
        now.return_value = django_now()
        end_date = datetime.datetime(year=now().year + 1, month=now().month,
            day=now().day, hour=now().hour, minute=now().minute,
            second=now().second, microsecond=now().microsecond, tzinfo=utc)
        request = mock.Mock()
        request.user.membership.end_date = end_date

        # action
        returned_value = wrapped_view(request, *self.args, **self.kwargs)

        # assert
        self.assertTupleEqual(((request,) + self.args, self.kwargs,),
            view.call_args)
        self.assertEqual(id(view.return_value), id(returned_value))
        self.assertTupleEqual(('CURRENT', True,),
            returned_value.__setitem__.call_args[0])

    @mock.patch('membership.decorators.redirect')
    def test_enforce_membership_should_redirect_to_membership_area_when_the_user_doesnt_have_a_membership(
            self, redirect):
        # setup
        class UserMock(mock.Mock):
            @property
            def membership(self):
                raise Membership.DoesNotExist()

        view = mock.Mock()
        wrapped_view = enforce_membership(view)
        request = mock.Mock()
        request.user = UserMock()

        # action
        returned_value = wrapped_view(request)

        # assert
        self.assertTupleEqual(('membership:home',), redirect.call_args[0])
        self.assertEqual(0, view.call_count)
        self.assertEqual(id(redirect.return_value), id(returned_value))

    @mock.patch('membership.decorators.redirect')
    def test_enforce_membership_should_return_none_when_user_is_anonymous(self,
            redirect):
        # setup
        view = mock.Mock()
        wrapped_view = enforce_membership(view)
        request = mock.Mock()
        request.user = AnonymousUser()

        # action
        returned_value = wrapped_view(request)

        # assert
        self.assertTupleEqual(('membership:home',), redirect.call_args[0])
        self.assertEqual(0, view.call_count)
        self.assertEqual(id(redirect.return_value), id(returned_value))

    @mock.patch('membership.decorators.redirect')
    @mock.patch('membership.decorators.now')
    def test_enforce_membership_should_redirect_to_membership_home_when_users_membership_plan_has_expired(
            self, now, redirect):
        # setup
        view = mock.Mock()
        wrapped_view = enforce_membership(view)
        now.return_value = django_now()
        end_date = datetime.datetime(year=now().year - 3, month=now().month,
            day=now().day, hour=now().hour, minute=now().minute,
            second=now().second, microsecond=now().microsecond, tzinfo=utc)
        request = mock.Mock()
        request.user.membership.end_date = end_date

        # action
        returned_value = wrapped_view(request)

        # assert
        self.assertTupleEqual(('membership:home',), redirect.call_args[0])
        self.assertEqual(0, view.call_count)
        self.assertEqual(id(redirect.return_value), id(returned_value))

    def test_enforce_memberhsip_should_return_none_if_user_membership_plan_has_unlimited_duration(
            self):
        # setup
        view = mock.Mock(return_value=mock.MagicMock())
        wrapped_view = enforce_membership(view)
        request = mock.Mock()
        request.user.membership.plan_type.duration_unit = \
            constants.DURATION_UNIT_CHOICES.UNLIMITED

        # action
        returned_value = wrapped_view(request, *self.args, **self.kwargs)

        # assert
        self.assertTupleEqual(((request,) + self.args, self.kwargs,),
            view.call_args)
        self.assertEqual(id(view.return_value), id(returned_value))
        self.assertTupleEqual(('CURRENT', True,),
            returned_value.__setitem__.call_args[0])
