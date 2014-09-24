# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.urlresolvers import reverse
from django import forms

from libs import constants as lib_constants
from ..views import BusinessFormView


class BusinessFormViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_business_form(self):
        # setup
        view = BusinessFormView()
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
        self.assertTrue('number_offices' in form.fields.keys())
        self.assertTrue('is_mso' in form.fields.keys())
        self.assertTrue('number_employees' in form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = BusinessFormView()
        request = self.get_request()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'employer/business_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_get_initial_should_set_is_mso_as_yes(self):
        # setup
        view = BusinessFormView()

        # action
        returned_value = view.get_initial()

        # assert
        self.assertDictEqual(dict(is_mso=lib_constants.YES_NO_CHOICES.YES),
            returned_value)

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = BusinessFormView()

        # assert
        self.assertEqual('membership:home', view.success_url_alias)

    def get_request(self):
        request = mock.Mock()
        request.path = reverse('employer:business')
        request.META.get = mock.Mock(return_value='')
        return request
