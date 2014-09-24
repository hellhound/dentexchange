# -*- coding:utf-8 -*-
import mock
import unittest

from django.core.urlresolvers import reverse

from ..views import MembershipFormView


class MembershipFormViewTestCase(unittest.TestCase):
    def test_get_should_call_render_to_response_with_membership_form(self):
        # setup
        view = MembershipFormView()
        view.render_to_response = mock.Mock()
        request = self.get_request()
        view.request = request

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        self.assertTrue('billing_info_form' in context.keys())
        form = context['form']
        billing_info_form = context['billing_info_form']
        # Plan type
        self.assertTrue('plan_type' in form.fields.keys())
        # Purchase Information
        self.assertTrue('coupon_code' in form.fields.keys())
        # Contact Information
        self.assertTrue('first_name' in form.fields.keys())
        self.assertTrue('last_name' in form.fields.keys())
        self.assertTrue('email' in form.fields.keys())
        # Billing Address
        self.assertTrue('address' in form.fields.keys())
        self.assertTrue('zip_code' in form.fields.keys())
        self.assertTrue('city' in form.fields.keys())
        self.assertTrue('state' in form.fields.keys())
        self.assertTrue('country' in form.fields.keys())
        # Billing Info
        self.assertTrue('credit_card' in billing_info_form.fields.keys())
        self.assertTrue('cvv' in billing_info_form.fields.keys())
        self.assertTrue('expiry_month' in billing_info_form.fields.keys())
        self.assertTrue('expiry_year' in billing_info_form.fields.keys())

    def test_get_should_call_template_response_with_template(self):
        # setup
        view = MembershipFormView()
        request = self.get_request()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'membership/membership_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = MembershipFormView()

        # assert
        self.assertEqual('employee:dashboard', view.success_url_alias)

    @mock.patch('membership.views.Plan')
    @mock.patch('membership.views.BillingInfoForm')
    @mock.patch('membership.views.CreateView.get_context_data')
    def test_get_context_data_should_add_plans_to_the_context(self,
            get_context_data, billin_info_form_class, plan_class):
        # setup
        view = MembershipFormView()
        request = mock.Mock()
        request.user.userregistration.is_employer = mock.Mock()
        view.request = request
        get_context_data.return_value = {}
        context = dict(billing_info_form=billin_info_form_class.return_value,
            plans=plan_class.objects.filter.return_value)

        # action
        returned_value = view.get_context_data()

        # assert
        self.assertDictEqual(
            dict(for_employer=request.user.userregistration.is_employer),
            plan_class.objects.filter.call_args[1])
        self.assertDictEqual(context, returned_value)

    @mock.patch('membership.views.reverse')
    def test_get_success_url_should_redirect_to_employers_dashboard_if_user_is_employer(
            self, reverse):
        # setup
        view = MembershipFormView()
        request = mock.Mock()
        request.user.userregistration.is_employer = True
        view.request = request

        # action
        returned_value = view.get_success_url()

        # assert
        self.assertTupleEqual(('employer:dashboard',), reverse.call_args[0])
        self.assertEqual(id(reverse.return_value), id(returned_value))

    @mock.patch('membership.views.SuccessURLAliasViewMixin.get_success_url')
    def test_get_success_url_return_super_if_user_is_employee(
            self, get_success_url):
        # setup
        view = MembershipFormView()
        request = mock.Mock()
        request.user.userregistration.is_employer = False
        view.request = request

        # action
        returned_value = view.get_success_url()

        # assert
        self.assertEqual(id(get_success_url.return_value), id(returned_value))

    def get_request(self):
        request = mock.Mock()
        request.path = reverse('membership:home')
        request.META.get = mock.Mock(return_value='')
        return request
