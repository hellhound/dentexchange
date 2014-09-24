# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.urlresolvers import reverse

from ..views import FirstPraxisFormView


class FirstPraxisFormViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_praxis_form(self):
        # setup
        view = FirstPraxisFormView()
        view.render_to_response = mock.Mock()
        request = self.get_request()
        view.request = request

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        ### Contact Info
        self.assertTrue('company_name' in form.fields.keys())
        self.assertTrue('contact_first_name' in form.fields.keys())
        self.assertTrue('contact_last_name' in form.fields.keys())
        ### Praxis Location
        self.assertTrue('address' in form.fields.keys())
        self.assertTrue('zip_code' in form.fields.keys())
        self.assertTrue('city' in form.fields.keys())
        self.assertTrue('state' in form.fields.keys())
        ### Type of Practice
        self.assertTrue('solo_practitioner' in form.fields.keys())
        self.assertTrue('multi_practitioner' in form.fields.keys())
        self.assertTrue('corporate' in form.fields.keys())
        ### Patients' Method of Payment
        self.assertTrue('fee_for_service' in form.fields.keys())
        self.assertTrue('insurance' in form.fields.keys())
        self.assertTrue('capitation_medicaid' in form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = FirstPraxisFormView()
        request = self.get_request()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'employer/first_praxis_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = FirstPraxisFormView()

        # assert
        self.assertEqual('employer:praxis_profile', view.success_url_alias)

    def get_request(self):
        request = mock.Mock()
        request.path = reverse('employer:first_praxis')
        request.META.get = mock.Mock(return_value='')
        return request
