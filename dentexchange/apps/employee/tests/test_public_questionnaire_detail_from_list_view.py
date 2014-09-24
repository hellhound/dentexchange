# -*- coding:utf-8 -*-
import unittest
import mock

from django.http.response import Http404

from ..views import PublicQuestionnaireDetailFromListView
from ..models import EmployeeQuestionnaire


class PublicQuestionnaireDetailFromListViewTestCase(unittest.TestCase):
    def test_model_should_reference_job_posting_model(self):
        # setup
        view = PublicQuestionnaireDetailFromListView()

        # assert
        self.assertEqual(id(EmployeeQuestionnaire), id(view.model))

    def test_should_call_template_response_with_template(self):
        # setup
        view = PublicQuestionnaireDetailFromListView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=EmployeeQuestionnaire())
        template_name = \
            'employee/public_questionnaire_detail_from_list.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('employee.views.EmployeeQuestionnaire.objects.get')
    def test_get_object_should_return_questionnaire_from_pk(self, get):
        # setup
        view = PublicQuestionnaireDetailFromListView()
        pk = 1
        request = mock.Mock()
        request.GET = dict(pk=pk)
        view.request = request

        # action
        returned_value = view.get_object()

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertEqual(id(get.return_value), id(returned_value))

    @mock.patch('employee.views.EmployeeQuestionnaire')
    def test_get_object_should_raise_http404_exception_when_pk_is_invalid(
            self, questionnaire_class):
        # setup
        view = PublicQuestionnaireDetailFromListView()
        pk = 1
        request = mock.Mock()
        request.GET = dict(pk=pk)
        view.request = request
        questionnaire_class.DoesNotExist = EmployeeQuestionnaire.DoesNotExist
        questionnaire_class.objects.get.side_effect = \
            EmployeeQuestionnaire.DoesNotExist

        # action
        with self.assertRaises(Http404):
            view.get_object()

        # assert
        self.assertDictEqual(dict(pk=pk),
            questionnaire_class.objects.get.call_args[1])
