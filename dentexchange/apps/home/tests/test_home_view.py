# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.exceptions import ObjectDoesNotExist

from ..views import HomeView
from registration.models import UserRegistration


class HomeViewTestCase(unittest.TestCase):
    def test_get_user_registration_should_user_registration(self):
        # setup
        view = HomeView()
        request = mock.Mock()
        view.request = request

        # action
        returned_value = view.get_user_registration()

        # assert
        self.assertEqual(id(request.user.userregistration), id(returned_value))

    @mock.patch('home.views.UserRegistration')
    @mock.patch('home.views.reverse')
    def test_get_redirect_url_should_return_registration_home_url_when_unregistered_logged_in_user(
            self, reverse, user_registration_class):
        # setup
        view = HomeView()
        request = mock.Mock()
        view.request = request
        user_registration_class.DoesNotExist = ObjectDoesNotExist
        view.get_user_registration = mock.Mock(
            side_effect=user_registration_class.DoesNotExist)

        # action
        returned_value = view.get_redirect_url()

        # assert
        self.assertTupleEqual(('registration:home',), reverse.call_args[0])
        self.assertEqual(id(reverse.return_value), id(returned_value))

    @mock.patch('home.views.reverse')
    def test_get_redirect_url_should_return_employer_dashboard_url_when_user_is_employer(
            self, reverse):
        # setup
        view = HomeView()
        request = mock.Mock()
        request.user.userregistration.is_employer = True
        view.request = request

        # action
        returned_value = view.get_redirect_url()

        # assert
        self.assertTupleEqual(('employer:dashboard',), reverse.call_args[0])
        self.assertEqual(id(reverse.return_value), id(returned_value))

    @mock.patch('home.views.reverse')
    def test_get_redirect_url_should_return_employee_dashboard_url_when_user_is_employee(
            self, reverse):
        # setup
        view = HomeView()
        request = mock.Mock()
        request.user.userregistration.is_employer = False
        view.request = request

        # action
        returned_value = view.get_redirect_url()

        # asert
        self.assertTupleEqual(('employee:dashboard',), reverse.call_args[0])
        self.assertEqual(id(reverse.return_value), id(returned_value))
