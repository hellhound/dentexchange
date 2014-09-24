# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.urlresolvers import reverse

from ..views import RegistrationFormView


class RegistrationFormViewTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaned_data = dict(email='email', password='password',
            is_employer=False)

    def test_get_should_call_render_to_response_with_registration_form(self):
        # setup
        view = RegistrationFormView()
        view.render_to_response = mock.Mock()
        request = self.get_request()
        view.request = request

        # action
        response = view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        self.assertTrue('email' in form.fields.keys())
        self.assertTrue('is_employer' in form.fields.keys())
        self.assertTrue('password' in form.fields.keys())
        self.assertTrue('confirm_password' in form.fields.keys())
        self.assertTrue('terms_of_use' in form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = RegistrationFormView()
        request = self.get_request()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'registration/registration_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = RegistrationFormView()

        # assert
        self.assertEqual('employee:questionnaire_signup_add',
            view.success_url_alias)

    @mock.patch('registration.views.send_welcome_message')
    @mock.patch('registration.views.login')
    @mock.patch('registration.views.authenticate')
    @mock.patch('registration.views.CreateView.form_valid')
    def test_form_valid_should_authenticate_user(self,
            form_valid, authenticate, login, send_welcome_message):
        # setup
        view = RegistrationFormView()
        request = mock.Mock()
        request.configure_mock(META=dict(HTTP_HOST='http_host'))
        view.request = request
        form = mock.Mock()
        cleaned_data = self.cleaned_data
        form.configure_mock(cleaned_data=cleaned_data)
        authenticate_args = dict(username=cleaned_data['email'],
            password=cleaned_data['password'])
        user = authenticate.return_value

        # action
        view.form_valid(form)

        # assert
        self.assertDictEqual(authenticate_args,
            authenticate.call_args[1])
        self.assertTupleEqual((request, user), login.call_args[0])

    @mock.patch('registration.views.redirect')
    @mock.patch('registration.views.send_welcome_message')
    @mock.patch('registration.views.login')
    @mock.patch('registration.views.authenticate')
    @mock.patch('registration.views.CreateView.form_valid')
    def test_form_valid_should_redirect_to_employer_business_after_authentication(
            self, form_valid, authenticate, login, send_welcome_message,
            redirect):
        # setup
        view = RegistrationFormView()
        request = mock.Mock()
        request.configure_mock(META=dict(HTTP_HOST='http_host'))
        view.request = request
        form = mock.Mock()
        cleaned_data = self.cleaned_data
        cleaned_data['is_employer'] = True
        form.configure_mock(cleaned_data=cleaned_data)
        authenticate_args = dict(username=cleaned_data['email'],
            password=cleaned_data['password'])
        user = authenticate.return_value

        # action
        returned_value = view.form_valid(form)

        # assert
        self.assertDictEqual(authenticate_args,
            authenticate.call_args[1])
        self.assertTupleEqual((request, user), login.call_args[0])
        self.assertTupleEqual(('employer:business',), redirect.call_args[0])
        self.assertEqual(id(redirect.return_value), id(returned_value))

    @mock.patch('registration.views.send_welcome_message')
    @mock.patch('registration.views.login')
    @mock.patch('registration.views.authenticate')
    @mock.patch('registration.views.CreateView.form_valid')
    def test_form_valid_should_send_welcome_message_email(self,
            form_valid, authenticate, login, send_welcome_message):
        # setup
        view = RegistrationFormView()
        host = 'somehost'
        request = mock.Mock()
        request.configure_mock(META=dict(HTTP_HOST=host))
        view.request = request
        form = mock.Mock()
        form.configure_mock(cleaned_data=self.cleaned_data)

        # action
        response = view.form_valid(form)

        # assert
        self.assertTupleEqual((host, self.cleaned_data['email'],),
            send_welcome_message.delay.call_args[0])
        self.assertEqual(id(form_valid.return_value), id(response))

    def get_request(self):
        request = mock.Mock()
        request.path = reverse('registration:home')
        request.META.get = mock.Mock(return_value='')
        return request
