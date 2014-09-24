# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from employee.models import EmployeeQuestionnaire
from ..views import AddQuestionnaireMatchView


class AddQuestionnaireMatchViewTestCase(unittest.TestCase):
    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.Match.objects.create')
    @mock.patch('matches.views.EmployeeQuestionnaire.objects.get')
    def test_get_ajax_should_create_match_with_questionnaire_and_return_status_ok(
            self, get, create, render_json_response):
        # setup
        view = AddQuestionnaireMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='ok')

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertDictEqual(dict(user=user, match=get.return_value),
            create.call_args[1])
        self.assertTupleEqual((context,), render_json_response.call_args[0])
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.EmployeeQuestionnaire.objects.get')
    def test_get_ajax_should_return_bad_request_response_when_pk_doesnt_exists(
            self, get, render_json_response):
        # setup
        view = AddQuestionnaireMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='error')
        get.side_effect = EmployeeQuestionnaire.DoesNotExist

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertTupleEqual(((context,), dict(status=400),),
            render_json_response.call_args)
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))

    @mock.patch('matches.views.views.JSONResponseMixin.render_json_response')
    @mock.patch('matches.views.EmployeeQuestionnaire.objects.get')
    def test_get_ajax_should_return_bad_request_response_when_multiple_pk(
            self, get, render_json_response):
        # setup
        view = AddQuestionnaireMatchView()
        user = User()
        request = mock.Mock()
        pk = 1
        request.GET = dict(pk=pk)
        request.user = user
        view.request = request
        context = dict(status='error')
        get.side_effect = EmployeeQuestionnaire.MultipleObjectsReturned

        # action
        returned_value = view.get_ajax(request)

        # assert
        self.assertDictEqual(dict(pk=pk), get.call_args[1])
        self.assertTupleEqual(((context,), dict(status=400),),
            render_json_response.call_args)
        self.assertEqual(id(render_json_response.return_value),
            id(returned_value))
