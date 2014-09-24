# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import DashboardView


class DashboardViewTestCase(unittest.TestCase):
    def test_get_should_call_template_response_with_template(self):
        # setup
        view = DashboardView()
        request = mock.Mock()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'employee/dashboard.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('employee.views.Match.objects.filter')
    @mock.patch('employee.views.TemplateView.get_context_data')
    def test_get_context_data_should_add_user_matches(
            self, get_context_data, match_filter):
        # setup
        view = DashboardView()
        user = mock.Mock()
        request = mock.Mock()
        request.user = user
        view.request = request
        get_context_data.return_value = {}

        # action
        returned_value = view.get_context_data()

        # assert
        self.assertDictEqual(dict(user=user), match_filter.call_args[1])
        self.assertEqual(id(match_filter.return_value),
            id(returned_value['matches']))
        self.assertEqual(id(get_context_data.return_value), id(returned_value))
