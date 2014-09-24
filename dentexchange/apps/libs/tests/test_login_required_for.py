# -*- coding:utf-8 -*-
import unittest
import mock

from ..decorators import login_required_for, EMPLOYER, EMPLOYEE


class LoginRequiredForTestCase(unittest.TestCase):
    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_employer_return_user_passes_test_with_check_returning_true(
            self, user_passes_test):
        # setup
        user = mock.Mock()
        user.userregistration.is_employer = True

        # action
        returned_value = login_required_for(EMPLOYER)

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertTrue(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))

    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_employee_return_user_passes_test_with_check_returning_true(
            self, user_passes_test):
        # setup
        user = mock.Mock()
        user.userregistration.is_employer = False

        # action
        returned_value = login_required_for(EMPLOYEE)

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertTrue(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))

    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_employer_return_user_passes_test_with_check_returning_false(
            self, user_passes_test):
        # setup
        user = mock.Mock()
        user.userregistration.is_employer = False

        # action
        returned_value = login_required_for(EMPLOYER)

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertFalse(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))

    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_employee_return_user_passes_test_with_check_returning_false(
            self, user_passes_test):
        # setup
        user = mock.Mock()
        user.userregistration.is_employer = True

        # action
        returned_value = login_required_for(EMPLOYEE)

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertFalse(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))

    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_should_return_false_if_user_doesnt_have_userregistration_attr(
            self, user_passes_test):
        # setup
        user = object()

        # action
        returned_value = login_required_for(EMPLOYER)

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertFalse(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))

    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_should_return_user_passes_test_with_check_returning_false_for_login_types_list(
            self, user_passes_test):
        # setup
        user = mock.Mock()
        user.userregistration.is_employer = False

        # action
        returned_value = login_required_for((EMPLOYER, EMPLOYER,))

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertFalse(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))

    @mock.patch('libs.decorators.user_passes_test')
    def test_login_required_for_should_return_user_passes_test_with_check_returning_true_for_login_types_list(
            self, user_passes_test):
        # setup
        user = mock.Mock()
        user.userregistration.is_employer = False

        # action
        returned_value = login_required_for((EMPLOYER, EMPLOYEE,))

        # assert
        check = user_passes_test.call_args[0][0]
        passes = check(user)
        self.assertTrue(passes)
        self.assertEqual(id(user_passes_test.return_value), id(returned_value))
