# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import DeletePostingView
from ..models import JobPosting


class DeletePostingViewTestCase(unittest.TestCase):
    @mock.patch('employer.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('employer.views.JobPosting.objects.get')
    def test_get_ajax_should_delete_praxis_and_return_status_ok(
            self, get, render_json_response):
        # setup
        view = DeletePostingView()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        view.request = request
        context = dict(status='ok')

        # action
        returned_value = view.get_ajax(request)
        
        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertEqual(1, get.return_value.delete.call_count)
        self.assertTupleEqual((context,), render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('employer.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('employer.views.JobPosting.objects.get')
    def test_get_ajax_should_return_bad_request_response_when_pk_doesnt_exist(
            self, get, render_json_response):
        # setup
        view = DeletePostingView()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        view.request = request
        context = dict(status='error')
        get.side_effect = JobPosting.DoesNotExist

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertTupleEqual(((context,), dict(status=400),),
            render_json_response.call_args)
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))
