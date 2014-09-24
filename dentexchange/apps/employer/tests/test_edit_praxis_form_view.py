# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.urlresolvers import reverse

from ..views import EditPraxisFormView
from ..models import Praxis


class EditPraxisFormViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_praxis_form(self):
        # setup
        view = EditPraxisFormView()
        request = mock.Mock()
        view.request = request
        view.render_to_response = mock.Mock()
        view.get_object = mock.Mock(return_value=Praxis())

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
        view = EditPraxisFormView()
        request = mock.Mock()
        view.request = request
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=Praxis())
        template_name = 'employer/edit_praxis_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_get_sucess_url_should_redirect_to_success_url(self):
        # setup
        view = EditPraxisFormView()
        view.object = mock.Mock()
        view.object.configure_mock(pk='1')

        # action
        returned_value = view.get_success_url()

        # assert
        self.assertEqual(reverse('employer:job_posting_list',
            args=(view.object.pk,)), returned_value)
