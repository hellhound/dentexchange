# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import PraxisProfileView
from ..models import Praxis


class PraxisProfileViewTestCase(unittest.TestCase):
    def test_model_should_reference_praxis_model(self):
        # setup
        view = PraxisProfileView()

        # assert
        self.assertEqual(id(Praxis), id(view.model))

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = PraxisProfileView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        template_name = 'employer/praxis_profile.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('employer.views.DentexchangeListView.get_queryset')
    def test_get_queryset_should_return_filtered_queryset_by_user(
            self, get_queryset):
        # setup
        view = PraxisProfileView()
        request = mock.Mock()
        request.configure_mock(user=mock.Mock())
        view.request = request

        # action
        returned_value = view.get_queryset()

        # assert
        self.assertDictEqual(dict(business__user=request.user),
            get_queryset.return_value.filter.call_args[1])
        self.assertEqual(id(get_queryset.return_value.filter.return_value),
            id(returned_value))
