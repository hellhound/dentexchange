# -*- coding:utf-8 -*-
import unittest
import mock

from django.http.response import Http404

from employee import constants as employee_constants
from ..views import AddNewPostingFormView
from ..models import Praxis
from libs import constants as lib_constants


class AddNewPostingFormViewTestCase(unittest.TestCase):
    @mock.patch('employer.views.Praxis.objects.get')
    def test_get_should_call_render_to_response_with_job_posting_form(self,
            get):
        # setup
        view = AddNewPostingFormView()
        view.render_to_response = mock.Mock()
        request = mock.Mock()
        view.request = request
        view.kwargs = {}

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.render_to_response.call_count)
        context = view.render_to_response.call_args[0][0]
        self.assertTrue('form' in context.keys())
        form = context['form']
        ### Contact Info
        self.assertTrue('position_name' in form.fields.keys())
        self.assertTrue('posting_title' in form.fields.keys())
        ### Job posting you are offering
        self.assertTrue('job_position' in form.fields.keys())
        ### Type of schedule required
        self.assertTrue('schedule_type' in form.fields.keys())
        self.assertTrue('monday_daytime' in form.fields.keys())
        self.assertTrue('monday_evening' in form.fields.keys())
        self.assertTrue('tuesday_daytime' in form.fields.keys())
        self.assertTrue('tuesday_evening' in form.fields.keys())
        self.assertTrue('wednesday_daytime' in form.fields.keys())
        self.assertTrue('wednesday_evening' in form.fields.keys())
        self.assertTrue('thursday_daytime' in form.fields.keys())
        self.assertTrue('thursday_evening' in form.fields.keys())
        self.assertTrue('friday_daytime' in form.fields.keys())
        self.assertTrue('friday_evening' in form.fields.keys())
        self.assertTrue('saturday_daytime' in form.fields.keys())
        self.assertTrue('saturday_evening' in form.fields.keys())
        self.assertTrue('sunday_daytime' in form.fields.keys())
        self.assertTrue('sunday_evening' in form.fields.keys())
        ### Compensation
        self.assertTrue('compensation_type' in form.fields.keys())
        self.assertTrue('hourly_wage' in form.fields.keys())
        self.assertTrue('annualy_wage' in form.fields.keys())
        self.assertTrue('production' in form.fields.keys())
        self.assertTrue('collection' in form.fields.keys())
        ### Experience required
        self.assertTrue('experience_years' in form.fields.keys())
        ### Benefits being offered
        self.assertTrue('benefit_1' in form.fields.keys())
        self.assertTrue('benefit_2' in form.fields.keys())
        self.assertTrue('benefit_3' in form.fields.keys())
        self.assertTrue('benefit_4' in form.fields.keys())
        self.assertTrue('benefit_5' in form.fields.keys())
        self.assertTrue('benefit_6' in form.fields.keys())
        self.assertTrue('benefit_other' in form.fields.keys())
        self.assertTrue('benefit_other_text' in form.fields.keys())
        self.assertTrue('visa' in form.fields.keys())
        self.assertTrue('additional_comments' in form.fields.keys())

    @mock.patch('employer.views.Praxis.objects.get')
    def test_get_should_call_template_response_with_template(self, get):
        # setup
        view = AddNewPostingFormView()
        request = mock.Mock()
        view.request = request
        view.response_class = mock.Mock()
        view.kwargs = {}
        template_name = 'employer/add_new_posting_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    @mock.patch('employer.views.CreateView.form_valid')
    @mock.patch('employer.views.MembershipRestrictionAdapter')
    def test_form_valid_should_call_membership_restriction_adapters_apply_job_posting_restrictions_and_redirect_to_success_url(
            self, restriction_adapter_class, form_valid):
        # setup
        view = AddNewPostingFormView()
        restriction_adapter = restriction_adapter_class.return_value
        form = mock.Mock()
        request = mock.Mock()
        view.request = request

        # action
        view.form_valid(form)

        # assert
        self.assertEqual('employer:praxis_profile', view.success_url_alias)
        self.assertTupleEqual((request.user.membership,),
            restriction_adapter_class.call_args[0])
        self.assertEqual(1,
            restriction_adapter.apply_job_posting_restrictions.call_count)
        self.assertTupleEqual((form,), form_valid.call_args[0])


    @mock.patch('employer.views.Praxis.objects.get')
    @mock.patch(
        'employer.views.AddNewPostingFormView.dispatch_if_restriction_is_valid')
    def test_dispatch_should_set_praxis(self, dispatch, get):
        # setup
        view = AddNewPostingFormView()
        praxis_pk = '1'
        view.kwargs = dict(pk=praxis_pk)
        request = mock.Mock()

        # action
        returned_value = view.dispatch(request)

        # assert
        self.assertDictEqual(dict(pk=praxis_pk), get.call_args[1])
        self.assertEqual(id(view.praxis), id(get.return_value))
        self.assertTupleEqual((request,), dispatch.call_args[0])
        self.assertEqual(id(dispatch.return_value), id(returned_value))

    @mock.patch('employer.views.Praxis')
    @mock.patch('employer.views.CreateView.get_form_kwargs')
    def test_dispatch_should_raise_http404_when_praxis_doesnt_exist(
            self, get_form_kwargs, praxis_class):
        # setup
        view = AddNewPostingFormView()
        view.kwargs = dict(pk='1')
        request = mock.Mock()
        praxis_class.DoesNotExist = Praxis.DoesNotExist
        praxis_class.objects.get.side_effect = Praxis.DoesNotExist

        # action and assert
        with self.assertRaises(Http404) as cm:
            view.dispatch(request)

    @mock.patch('employer.views.CreateView.dispatch')
    @mock.patch('employer.views.MembershipRestrictionAdapter')
    def test_dispatch_if_restriction_is_valid_should_return_super_dispatch_when_membership_restriction_adapters_verify_job_posting_restrictions_returns_true(
            self, restriction_adapter_class, dispatch):
        # setup
        view = AddNewPostingFormView()
        request = mock.Mock()
        restriction_adapter = restriction_adapter_class.return_value
        restriction_adapter.verify_job_posting_restrictions.return_value = True

        # action
        returned_value = view.dispatch_if_restriction_is_valid(request)

        # assert
        self.assertTupleEqual((request.user.membership,),
            restriction_adapter_class.call_args[0])
        self.assertEqual(1,
            restriction_adapter.verify_job_posting_restrictions.call_count)
        self.assertTupleEqual((request,), dispatch.call_args[0])
        self.assertEqual(id(dispatch.return_value), id(returned_value))

    @mock.patch('employer.views.AddNewPostingFormView.render_to_response')
    @mock.patch('employer.views.AddNewPostingFormView.get_context_data')
    @mock.patch('employer.views.AddNewPostingFormView.get_form')
    @mock.patch('employer.views.AddNewPostingFormView.get_form_class')
    @mock.patch('employer.views.MembershipRestrictionAdapter')
    def test_dispatch_if_restriction_is_valid_should_add_warning_message_to_request_and_return_render_to_response_with_form_when_membership_restriction_adapters_verify_job_posting_restrictions_returns_false(
            self, restriction_adapter_class, get_form_class, get_form,
            get_context_data, render_to_response):
        # setup
        view = AddNewPostingFormView()
        request = mock.Mock()
        restriction_adapter = restriction_adapter_class.return_value
        restriction_adapter.verify_job_posting_restrictions.return_value = False

        # action
        returned_value = view.dispatch_if_restriction_is_valid(request)

        # assert
        self.assertTupleEqual((request.user.membership,),
            restriction_adapter_class.call_args[0])
        self.assertEqual(1,
            restriction_adapter.verify_job_posting_restrictions.call_count)
        self.assertEqual(1, get_form_class.call_count)
        self.assertTupleEqual((get_form_class.return_value,),
            get_form.call_args[0])
        self.assertDictEqual(dict(form=get_form.return_value),
            get_context_data.call_args[1])
        self.assertTupleEqual((get_context_data.return_value,),
            render_to_response.call_args[0])
        self.assertEqual(id(render_to_response.return_value),
            id(returned_value))

    @mock.patch('employer.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_put_praxis_pk_into_kwargs_and_return_kwargs(
            self, get_form_kwargs):
        # setup
        view = AddNewPostingFormView()
        view.praxis = mock.Mock()
        view.request = mock.Mock()
        get_form_kwargs.return_value = {}

        # action
        kwargs = view.get_form_kwargs()

        # assert
        self.assertEqual(view.praxis, kwargs['praxis'])

    @mock.patch('employer.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_assign_is_posted_to_true(self,
            get_form_kwargs):
        # setup
        view = AddNewPostingFormView()
        request = mock.Mock()
        request.POST = dict(_post_now='_post_now')
        view.request = request
        get_form_kwargs.return_value = {}

        # action
        kwargs = view.get_form_kwargs()

        # assert
        self.assertTrue(kwargs['is_posted'])

    @mock.patch('employer.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_assign_is_posted_to_false(self,
            get_form_kwargs):
        # setup
        view = AddNewPostingFormView()
        view.kwargs = dict(pk='1')
        request = mock.Mock()
        request.POST = {}
        view.request = request
        get_form_kwargs.return_value = {}

        # action
        kwargs = view.get_form_kwargs()

        # assert
        self.assertFalse(kwargs['is_posted'])

    def test_get_initial_should_set_schedule_type_and_compensation_type_as_part_time(
            self):
        # setup
        view = AddNewPostingFormView()

        # action
        initial = view.get_initial()

        # assert
        self.assertDictEqual(dict(
            schedule_type=\
                employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME, 
            compensation_type=\
                employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY,
            visa=lib_constants.YES_NO_CHOICES.YES),
            initial)
