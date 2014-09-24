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
        template_name = 'employer/dashboard.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])
