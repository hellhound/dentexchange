# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404

from ..views import JobPostingListView
from ..models import JobPosting, Praxis


class EmployerQuestionnaireListViewTestCase(unittest.TestCase):
    def test_model_should_reference_job_posting_model(self):
        # setup
        view = JobPostingListView()

        # assert
        self.assertEqual(id(JobPosting), id(view.model))

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = JobPostingListView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_queryset = mock.Mock()
        template_name = 'employer/job_posting_list.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('employer.views.Praxis.objects.get')
    @mock.patch('employer.views.DentexchangeListView.get_queryset')
    def test_get_queryset_should_return_queryset_when_praxis_is_valid(
            self, get_queryset, get):
        # setup
        view = JobPostingListView()
        praxis_pk = '1'
        view.kwargs = dict(pk=praxis_pk)

        # action
        returned_value = view.get_queryset()

        # assert
        self.assertDictEqual(dict(pk=praxis_pk), get.call_args[1])
        self.assertDictEqual(dict(praxis=get.return_value),
            get_queryset.return_value.filter.call_args[1])
        self.assertEqual(id(get_queryset.return_value.filter.return_value),
            id(returned_value))

    @mock.patch('employer.views.Praxis.objects.get')
    @mock.patch('employer.views.DentexchangeListView.get_queryset')
    def test_get_queryset_should_raise_http404_when_praxis_is_invalid(
            self, get_queryset, get):
        # setup
        view = JobPostingListView()
        praxis_pk = '1'
        view.kwargs = dict(pk=praxis_pk)
        Praxis.DoesNotExist = ObjectDoesNotExist
        get.side_effect = Praxis.DoesNotExist

        # action and assert
        with self.assertRaises(Http404) as cm:
            view.get_queryset()

    @mock.patch('employer.views.DentexchangeListView.get_context_data')
    @mock.patch('employer.views.JobPostingListView.praxis')
    def test_get_context_data_should_put_praxis_into_context_and_return_context(
            self, praxis, get_context_data):
        # setup
        view = JobPostingListView()
        praxis_pk = '1'
        view.kwargs = dict(pk=praxis_pk)
        praxis_value = 'praxis'
        praxis.__get__ = mock.Mock(return_value=praxis_value)
        get_context_data.return_value = {}

        # action
        returned_value = view.get_context_data()

        # assert
        self.assertDictEqual(dict(praxis=praxis_value), returned_value)
        self.assertEqual(id(get_context_data.return_value), id(returned_value))
