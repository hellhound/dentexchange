# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..views import DeleteJobPostingMatchView
from ..models import Match
from employer.models import JobPosting


class DeleteJobPostingMatchViewTestCase(unittest.TestCase):
    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.JobPosting.objects.get')
    def test_get_ajax_should_create_match_with_job_posting_and_return_status_ok(
            self, get, render_json_response):
        # setup
        view = DeleteJobPostingMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='ok', total=0)
        matching_object = get.return_value
        match = matching_object.matches.get.return_value

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertDictEqual(dict(user=user),
            matching_object.matches.get.call_args[1])
        self.assertEqual(1, match.delete.call_count)
        self.assertTupleEqual((context,), render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.JobPosting.objects.get')
    def test_get_ajax_should_return_bad_request_response_when_pk_doesnt_exist(
            self, get, render_json_response):
        # setup
        view = DeleteJobPostingMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='error')
        get.side_effect = JobPosting.DoesNotExist

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertTupleEqual(((context,), dict(status=400),),
            render_json_response.call_args)
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.JobPosting.objects.get')
    def test_get_ajax_should_return_bad_request_response_when_multiple_pk(
            self, get, render_json_response):
        # setup
        view = DeleteJobPostingMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='error')
        get.side_effect = JobPosting.MultipleObjectsReturned

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertTupleEqual(((context,), dict(status=400),),
            render_json_response.call_args)
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.JobPosting.objects.get')
    def test_get_ajax_should_return_bad_request_response_when_theres_no_match_for_matching_object(
            self, get, render_json_response):
        # setup
        view = DeleteJobPostingMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='error')
        matching_object = get.return_value
        matching_object.matches.get.side_effect = Match.DoesNotExist

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertDictEqual(dict(user=user),
            matching_object.matches.get.call_args[1])
        self.assertTupleEqual(((context,), dict(status=400),),
            render_json_response.call_args)
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))
