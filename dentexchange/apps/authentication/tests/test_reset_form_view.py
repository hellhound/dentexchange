# -*- coding:utf-8 -*-
import unittest
import mock

from ..views import ResetFormView


class ResetFormViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_reset_form(self):
        # setup
        view = ResetFormView()
        view.render_to_response = mock.Mock()
        request = mock.Mock()
        view.request = request

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        self.assertTrue('email' in form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = ResetFormView()
        request = mock.Mock()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'authentication/reset_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = ResetFormView()

        # assert
        self.assertEqual('authentication:successful_email_confirmation',
            view.success_url_alias)

    @mock.patch('authentication.views.FormView.form_valid')
    @mock.patch('authentication.views.send_confirmation')
    def test_form_valid_should_send_verification_email(self, send_confirmation, 
            form_valid):
        # setup
        view = ResetFormView()
        host = 'somehost'
        request = mock.Mock()
        request.configure_mock(META=dict(HTTP_HOST=host))
        view.request = request
        form = mock.Mock()
        cleaned_data = dict(email='an@example.com')
        form.configure_mock(cleaned_data=cleaned_data)

        # action
        response = view.form_valid(form)

        # assert
        self.assertTupleEqual((host, cleaned_data['email'],),
            send_confirmation.delay.call_args[0])
        self.assertEqual(id(form_valid.return_value), id(response))
