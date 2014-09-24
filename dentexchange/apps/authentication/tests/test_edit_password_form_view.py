# -*- coding:utf-8 -*-
import unittest
import mock

from django.contrib.auth.models import User

from ..views import EditPasswordFormView


class EditPasswordFormViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_registration_form(self):
        # setup
        view = EditPasswordFormView()
        request, token = self.get_request_and_token()
        view.request = request
        view.render_to_response = mock.Mock()
        view.get_object = mock.Mock(return_value=User())
        view.is_token_valid = mock.Mock(return_value=True)

        # action
        response = view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        self.assertTrue('password' in form.fields.keys())
        self.assertTrue('confirm_password' in form.fields.keys())
        self.assertTrue('token' in form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = EditPasswordFormView()
        request, token = self.get_request_and_token()
        view.request = request
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=User())
        view.is_token_valid = mock.Mock(return_value=True)
        template_name = 'authentication/edit_password_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = EditPasswordFormView()

        # assert
        self.assertEqual('main:home', view.success_url_alias)

    @mock.patch('authentication.views.redirect')
    @mock.patch('authentication.views.RecoveryToken.objects.is_token_valid')
    def test_get_should_redirect_to_expired_token_when_invalid_token(self,
            is_token_valid, redirect):
        # setup
        view = EditPasswordFormView()
        request, token = self.get_request_and_token()
        view.request = request
        is_token_valid.return_value = False

        # action
        response = view.get(request)

        # assert
        self.assertTupleEqual((token,), is_token_valid.call_args[0])
        self.assertTupleEqual(('authentication:expired_token',),
            redirect.call_args[0])
        self.assertEqual(id(redirect.return_value), id(response))

    @mock.patch('authentication.views.UpdateView.get')
    @mock.patch('authentication.views.RecoveryToken.objects.is_token_valid')
    def test_get_should_redirect_to_expired_token_when_valid_token(self,
            is_token_valid, get):
        # setup
        view = EditPasswordFormView()
        request, token = self.get_request_and_token()
        view.request = request
        is_token_valid.return_value = True

        # action
        response = view.get(request)

        # assert
        self.assertTupleEqual((token,), is_token_valid.call_args[0])
        self.assertEqual(id(get.return_value), id(response))

    def get_request_and_token(self):
        token = 'atoken'
        request = mock.Mock()
        request.configure_mock(GET=dict(token=token))
        return (request, token)

    @mock.patch('authentication.views.User.objects.get')
    def test_get_object_should_return_user_from_token(self, get):
        # setup
        view = EditPasswordFormView()
        request, token = self.get_request_and_token()
        view.request = request

        # action
        returned_value = view.get_object()

        # assert
        self.assertDictEqual(dict(recoverytoken__token=token), get.call_args[1])
        self.assertEqual(id(get.return_value), id(returned_value))

    @mock.patch('authentication.views.UpdateView.get_initial')
    def test_get_initial_should_assign_initial_token(self, get_initial):
        # setup
        view = EditPasswordFormView()
        request, token = self.get_request_and_token()
        view.request = request
        get_initial.return_value = {}

        # action
        returned_value = view.get_initial()

        # assert
        self.assertEqual(token, returned_value['token'])
