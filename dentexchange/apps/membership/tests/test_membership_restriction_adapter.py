# -*- coding:utf-8 -*-
import unittest
import mock

from ..utils import MembershipRestrictionAdapter


class MembershipRestrictionAdapterTestCase(unittest.TestCase):
    def setUp(self):
        user_registration = mock.Mock()
        user_registration.is_employer = True
        user = mock.Mock()
        user.userregistration = user_registration
        plan_type = mock.Mock()
        plan_type.total_allowed_job_postings = 3
        membership = mock.Mock()
        membership.user = user
        membership.plan_type = plan_type
        self.membership = membership

    def test_reset_restrictions_when_user_is_employer_should_reset_remaining_job_postings(
            self):
        # setup
        adapter = MembershipRestrictionAdapter(self.membership)

        # action
        adapter.reset_restrictions()

        # assert
        self.assertEqual(self.membership.plan_type.total_allowed_job_postings,
            self.membership.remaining_job_postings)
        self.assertEqual(1, self.membership.save.call_count)

    def test_reset_restrictions_when_user_is_employee_should_noop(
            self):
        # setup
        self.membership.user.userregistration.is_employer = False
        adapter = MembershipRestrictionAdapter(self.membership)

        # action
        adapter.reset_restrictions()

        # assert
        # TODO

    def test_apply_job_posting_restrictions_should_decrement_memberships_remaining_job_postings(
            self):
        # setup
        self.membership.remaining_job_postings = 1
        adapter = MembershipRestrictionAdapter(self.membership)

        # action
        adapter.apply_job_posting_restrictions()

        # assert
        self.assertEqual(0, self.membership.remaining_job_postings)
        self.assertEqual(1, self.membership.save.call_count)

    def test_apply_job_posting_restrictions_shouldnt_decrement_memberships_remaining_job_postings_when_its_0(
            self):
        # setup
        self.membership.remaining_job_postings = 0
        adapter = MembershipRestrictionAdapter(self.membership)

        # action
        adapter.apply_job_posting_restrictions()

        # assert
        self.assertEqual(0, self.membership.remaining_job_postings)

    def test_verify_job_posting_restrictions_should_return_true_when_available_job_postings(
            self):
        # setup
        self.membership.remaining_job_postings = 1
        adapter = MembershipRestrictionAdapter(self.membership)

        # action
        returned_value = adapter.verify_job_posting_restrictions()

        # assert
        self.assertTrue(returned_value)

    def test_verify_job_posting_restrictions_should_return_false_when_unavailable_job_postings(
            self):
        # setup
        self.membership.remaining_job_postings = 0
        adapter = MembershipRestrictionAdapter(self.membership)

        # action
        returned_value = adapter.verify_job_posting_restrictions()

        # assert
        self.assertFalse(returned_value)
