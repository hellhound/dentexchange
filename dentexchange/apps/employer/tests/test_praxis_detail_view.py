# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import PraxisDetailView
from ..models import Praxis


class PraxisDetailViewTestCase(unittest.TestCase):
    def test_model_should_reference_praxis_model(self):
        # setup
        view = PraxisDetailView()

        # assert
        self.assertEqual(id(Praxis), id(view.model))

    def test_should_call_template_response_with_template(self):
        # setup
        view = PraxisDetailView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=Praxis())
        template_name = 'employer/praxis_detail.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])
