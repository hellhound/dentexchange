# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import PostingDetailView
from ..models import JobPosting


class PostingDetailViewTestCase(unittest.TestCase):
    def test_model_should_reference_job_posting_model(self):
        # setup
        view = PostingDetailView()

        # assert
        self.assertEqual(id(JobPosting), id(view.model))

    def test_should_call_template_response_with_template(self):
        # setup
        view = PostingDetailView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=JobPosting())
        template_name = 'employer/posting_detail.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])
