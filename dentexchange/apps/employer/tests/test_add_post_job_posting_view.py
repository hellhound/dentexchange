# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.exceptions import ObjectDoesNotExist

from ..views import PostJobPostingView
from ..models import JobPosting


class PostJobPostingViewTestCase(unittest.TestCase):
    @mock.patch('employer.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('employer.views.JobPosting.objects.get')
    def test_get_ajax_should_set_is_posted_true_when_online_is_requested_and_return_status_ok(
            self, get, render_json_response):
        # setup
        view = PostJobPostingView()
        pk = '1'
        view.kwargs = dict(pk=pk, post_status='online')
        request = mock.Mock()
        instance = get.return_value

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertTrue(instance.is_posted)
        self.assertEqual(1, instance.save.call_count)
        self.assertTupleEqual((dict(status='ok'),),
            render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('employer.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('employer.views.JobPosting.objects.get')
    def test_get_ajax_should_set_is_posted_false_when_offline_is_requested_and_return_status_ok(
            self, get, render_json_response):
        # setup
        view = PostJobPostingView()
        pk = '1'
        view.kwargs = dict(pk=pk, post_status='offline')
        request = mock.Mock()
        instance = get.return_value

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertFalse(instance.is_posted)
        self.assertEqual(1, instance.save.call_count)
        self.assertTupleEqual((dict(status='ok'),),
            render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('employer.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('employer.views.JobPosting.objects.get')
    def test_get_ajax_should_return_status_error_upon_invalid_posting(
            self, get, render_json_response):
        # setup
        view = PostJobPostingView()
        pk = '1'
        view.kwargs = dict(pk=pk)
        request = mock.Mock()
        instance = get.return_value
        JobPosting.DoesNotExist = ObjectDoesNotExist
        get.side_effect = JobPosting.DoesNotExist

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertTupleEqual((dict(status='error'),),
            render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))
