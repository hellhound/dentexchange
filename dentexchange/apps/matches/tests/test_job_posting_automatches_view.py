# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import JobPostingAutomatchesView


class JobPostingAutomatchesViewTestCase(unittest.TestCase):
    def test_get_should_call_template_response_with_template(self):
        # setup
        view = JobPostingAutomatchesView()
        request = mock.Mock()
        view.request = request
        view.get_context_data = mock.Mock()
        view.response_class = mock.Mock()
        view.get_queryset = mock.Mock()
        template_name = 'matches/posting_automatches.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])
