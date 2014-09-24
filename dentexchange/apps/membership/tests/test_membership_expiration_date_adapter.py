# -*- coding:utf-8 -*-
import unittest
import mock
import datetime

from ..utils import MembershipExpirationDateAdapter
from .. import constants


class MembershipExpirationDateAdapterTestCase(unittest.TestCase):
    def setUp(self):
        plan_type = mock.Mock()
        plan_type.duration_magnitude = 3
        plan_type.duration_unit = constants.DURATION_UNIT_CHOICES.MONTHS
        self.membership = mock.Mock()
        self.membership.plan_type = plan_type

    @mock.patch('membership.utils.now')
    def test_save_end_date_should_save_memberships_end_date_on_the_same_day_but_for_the_plans_ending_period_on_same_year(
            self, utcnow):
        # setup
        adapter = MembershipExpirationDateAdapter(self.membership)
        utcnow.return_value = datetime.datetime(year=2014, month=3, day=14)
        end_date = datetime.datetime(year=2014, month=6, day=14)

        # action
        adapter.save_end_date()

        # assert
        self.assertEqual(1, self.membership.save.call_count)
        self.assertEqual(end_date, self.membership.end_date)

    @mock.patch('membership.utils.now')
    def test_save_end_date_should_save_memberships_end_date_on_the_same_day_but_for_the_plans_ending_period_on_different_year(
            self, utcnow):
        # setup
        adapter = MembershipExpirationDateAdapter(self.membership)
        utcnow.return_value = datetime.datetime(year=2014, month=11, day=14)
        end_date = datetime.datetime(year=2015, month=2, day=14)

        # action
        adapter.save_end_date()

        # assert
        self.assertEqual(1, self.membership.save.call_count)
        self.assertEqual(end_date, self.membership.end_date)

    @mock.patch('membership.utils.now')
    def test_save_end_date_should_save_memberships_end_date_on_last_day_of_calculated_month_for_the_plans_ending_period_if_date_is_invalid(
            self, utcnow):
        # setup
        self.membership.plan_type.duration_magnitude = 1
        adapter = MembershipExpirationDateAdapter(self.membership)
        utcnow.return_value = datetime.datetime(year=2014, month=1, day=31)
        end_date = datetime.datetime(year=2014, month=2, day=28)

        # action
        adapter.save_end_date()

        # assert
        self.assertEqual(1, self.membership.save.call_count)
        self.assertEqual(end_date, self.membership.end_date)

    @mock.patch('membership.utils.now')
    def test_save_end_date_should_save_memberships_end_date_on_same_date_for_the_next_year_when_plan_types_duration_unit_is_years_and_duration_magnitude_is_one(
            self, utcnow):
        # setup
        self.membership.plan_type.duration_magnitude = 1
        self.membership.plan_type.duration_unit = \
            constants.DURATION_UNIT_CHOICES.YEARS
        adapter = MembershipExpirationDateAdapter(self.membership)
        utcnow.return_value = datetime.datetime(year=2014, month=1, day=31)
        end_date = datetime.datetime(year=2015, month=1, day=31)

        # action
        adapter.save_end_date()

        # assert
        self.assertEqual(1, self.membership.save.call_count)
        self.assertEqual(end_date, self.membership.end_date)

    @mock.patch('membership.utils.now')
    def test_save_end_date_should_save_memberships_end_date_on_last_day_of_calculated_month_for_the_next_year_when_plan_types_duration_unit_is_years_and_duration_magnitude_is_one_and_if_date_is_invalid(
            self, utcnow):
        # setup
        self.membership.plan_type.duration_magnitude = 1
        self.membership.plan_type.duration_unit = \
            constants.DURATION_UNIT_CHOICES.YEARS
        adapter = MembershipExpirationDateAdapter(self.membership)
        utcnow.return_value = datetime.datetime(year=2000, month=2, day=29)
        end_date = datetime.datetime(year=2001, month=2, day=28)

        # action
        adapter.save_end_date()

        # assert
        self.assertEqual(1, self.membership.save.call_count)
        self.assertEqual(end_date, self.membership.end_date)

    def test_save_end_date_shouldnt_call_membership_save_if_plan_types_duration_unit_is_unlimited(
            self):
        # setup
        self.membership.plan_type.duration_unit = \
            constants.DURATION_UNIT_CHOICES.UNLIMITED
        adapter = MembershipExpirationDateAdapter(self.membership)

        # action
        adapter.save_end_date()

        # assert
        self.assertEqual(0, self.membership.save.call_count)
