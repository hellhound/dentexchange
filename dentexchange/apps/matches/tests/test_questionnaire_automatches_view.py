# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import QuestionnaireAutomatchesView


class QuestionnaireAutomatchesViewTestCase(unittest.TestCase):
    def test_get_should_call_template_response_with_template(self):
        # setup
        view = QuestionnaireAutomatchesView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_queryset = mock.Mock()
        template_name = 'matches/questionnaire_automatches.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

#   @mock.patch('matches.views.Praxis.objects.filter')
#   @mock.patch('matches.views.BaseAutomatchesView.get_context_data')
#   def test_get_context_data_should_return_context_with_all_user_praxes(
#           self, get_context_data, praxis_filter):
#       # setup
#       view = QuestionnaireAutomatchesView()
#       request = mock.Mock()
#       view.request = request
#       context = {}
#       get_context_data.return_value = context

#       # assert
#       returned_value = view.get_context_data(**{})

#       # action
#       self.assertDictEqual(dict(business__user=request.user),
#           praxis_filter.call_args[1])
#       self.assertEqual(id(praxis_filter.return_value), id(context['praxes']))
#       self.assertEqual(id(context), id(returned_value))
