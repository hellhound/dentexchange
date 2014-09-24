# -*- coding:utf-8 -*-
import unittest
import mock

from django.http.response import Http404

from ..views import PublicPostingDetailFromListView
from ..models import JobPosting


class PublicPostingDetailFromListTestCase(unittest.TestCase):
    def test_model_should_reference_job_posting_model(self):
        # setup
        view = PublicPostingDetailFromListView()

        # assert
        self.assertEqual(id(JobPosting), id(view.model))

    def test_should_call_template_response_with_template(self):
        # setup
        view = PublicPostingDetailFromListView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=JobPosting())
        template_name = 'employer/public_posting_detail_from_list.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('employer.views.JobPosting.objects.get')
    def test_get_object_should_return_posting_from_pk(self, get):
        # setup
        view = PublicPostingDetailFromListView()
        pk = 1
        request = mock.Mock()
        request.GET = dict(pk=pk)
        view.request = request

        # action
        returned_value = view.get_object()

        # assert
        self.assertDictEqual(dict(pk=pk, is_posted=True), get.call_args[1])
        self.assertEqual(id(get.return_value), id(returned_value))

    @mock.patch('employer.views.JobPosting')
    def test_get_object_should_raise_http404_exception_when_pk_is_invalid(
            self, job_posting_class):
        # setup
        view = PublicPostingDetailFromListView()
        pk = 1
        request = mock.Mock()
        request.GET = dict(pk=pk)
        view.request = request
        job_posting_class.DoesNotExist = JobPosting.DoesNotExist
        job_posting_class.objects.get.side_effect = JobPosting.DoesNotExist

        # action
        with self.assertRaises(Http404):
            view.get_object()

        # assert
        self.assertDictEqual(dict(pk=pk, is_posted=True),
            job_posting_class.objects.get.call_args[1])
