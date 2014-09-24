# -*- coding:utf-8 -*-
import unittest
import mock

from employee.models import EmployeeQuestionnaire
from ..views import QuestionnaireSavedMatchesView


class QuestionnaireSavedMatchesViewTestCase(unittest.TestCase):
    def test_get_query_should_return_all_user_matches(self):
        # setup
        view = QuestionnaireSavedMatchesView()
        request = mock.Mock()
        view.request = request

        # action
        returned_value = view.get_queryset()

        # assert
        self.assertEqual(1, request.user.match_set.all.call_count)
        self.assertEqual(id(request.user.match_set.all.return_value),
            id(returned_value))

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = QuestionnaireSavedMatchesView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_queryset = mock.Mock()
        template_name = 'matches/questionnaire_saved_matches.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])
