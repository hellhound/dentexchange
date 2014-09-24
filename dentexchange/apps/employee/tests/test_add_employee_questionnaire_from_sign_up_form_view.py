# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.urlresolvers import reverse
from django import forms

from ..views import AddEmployeeQuestionnaireFromSignUpFormView
from .. import constants
from libs import constants as lib_constants


class AddAddEmployeeQuestionnaireFromSignUpFormViewTestCase(unittest.TestCase):
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_get_should_call_render_to_response_with_questionnaire_form(
            self, resume_form):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
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
        ### Personal Info
        self.assertTrue('first_name' in form.fields.keys())
        self.assertTrue('last_name' in form.fields.keys())
        self.assertTrue('personal_address' in form.fields.keys())
        self.assertTrue('personal_zip_code' in form.fields.keys())
        self.assertTrue('personal_city' in form.fields.keys())
        self.assertTrue('personal_state' in form.fields.keys())
        ### Job Position you're looking for
        self.assertTrue('job_position' in form.fields.keys())
        ### Type of Practice
        self.assertTrue('solo_practitioner' in form.fields.keys())
        self.assertTrue('multi_practitioner' in form.fields.keys())
        self.assertTrue('corporate' in form.fields.keys())
        ### Patients' Method of Payment
        self.assertTrue('fee_for_service' in form.fields.keys())
        self.assertTrue('insurance' in form.fields.keys())
        self.assertTrue('capitation_medicaid' in form.fields.keys())
        ### Location
        self.assertTrue('zip_code' in form.fields.keys())
        self.assertTrue('city' in form.fields.keys())
        self.assertTrue('state' in form.fields.keys())
        self.assertTrue('distance' in form.fields.keys())
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
        ### Experience
        self.assertTrue('experience_years' in form.fields.keys())
        ### Education
        self.assertTrue('dental_school' in form.fields.keys())
        self.assertTrue('graduation_year' in form.fields.keys())
        ### Visa
        self.assertTrue('visa' in form.fields.keys())
        ### Specific Strengths
        self.assertTrue('specific_strengths' in form.fields.keys())
        ### Visibility
        self.assertTrue('is_private' in form.fields.keys())

    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_get_should_call_template_response_with_template(
            self, resume_form):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        request = self.get_request()
        view.request = request
        view.response_class = mock.Mock()
        template_name = 'employee/add_employee_questionnaire_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()

        # assert
        self.assertEqual('membership:home', view.success_url_alias)

    def test_get_initial_should_set_schedule_type_and_compensation_type_as_part_time(self):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()

        # action
        initial = view.get_initial()

        # assert
        self.assertDictEqual(dict(
            schedule_type=constants.SCHEDULE_TYPE_CHOICES.PART_TIME, 
            compensation_type=constants.COMPENSATION_TYPE_CHOICES.HOURLY,
            visa=lib_constants.YES_NO_CHOICES.YES),
            initial)

    @mock.patch('employee.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_return_kwargs_with_skippable_set_to_true_when_skip_is_present_in_post(
            self, get_form_kwargs):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        request = mock.Mock()
        request.POST = dict(_skip=True)
        view.request = request
        get_form_kwargs.return_value = {}

        # action
        returned_value = view.get_form_kwargs()

        # assert
        self.assertTrue(returned_value['skippable'])
        self.assertEqual(id(get_form_kwargs.return_value), id(returned_value))

    @mock.patch('employee.views.CreateView.get_form_kwargs')
    def test_get_form_kwargs_should_return_kwargs_with_skippable_set_to_false_when_skip_isnt_present_in_post(
            self, get_form_kwargs):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        request = mock.Mock()
        request.POST = {}
        view.request = request
        get_form_kwargs.return_value = {}

        # action
        returned_value = view.get_form_kwargs()

        # assert
        self.assertFalse(returned_value['skippable'])
        self.assertEqual(id(get_form_kwargs.return_value), id(returned_value))

    @mock.patch('employee.views.CreateView.render_to_response')
    @mock.patch('employee.views.CreateView.get_context_data')
    @mock.patch('employee.views.CreateView.get_form')
    def test_form_invalid_calls_render_to_response_with_skippable_and_form_as_context(self,
            get_form, get_context_data, render_to_response):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        form = mock.Mock()

        # action
        response = view.form_invalid(form)

        # assert
        self.assertEqual(1, get_form.return_value.is_valid.call_count)
        self.assertDictEqual(dict(skippable=False, form=form),
            get_context_data.call_args[1])
        self.assertTupleEqual((get_context_data.return_value,),
            render_to_response.call_args[0])
        self.assertEqual(id(render_to_response.return_value), id(response))

    @mock.patch('employee.views.CreateView.render_to_response')
    @mock.patch('employee.views.CreateView.get_context_data')
    @mock.patch('employee.views.CreateView.get_form')
    def test_form_invalid_sets_skippable_true_when_incomplete_form_validation_error_is_raised(self,
            get_form, get_context_data, render_to_response):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        form = mock.Mock()
        get_form.return_value.clean.configure_mock(
            side_effect=forms.ValidationError('',
            code=constants.QUESTIONNAIRE_FORM_INCOMPLETE_FORM_ERROR_CODE))

        # action
        response = view.form_invalid(form)

        # assert
        self.assertDictEqual(dict(skippable=True, form=form),
            get_context_data.call_args[1])

    @mock.patch('employee.views.CreateView.render_to_response')
    @mock.patch('employee.views.CreateView.get_context_data')
    @mock.patch('employee.views.CreateView.get_form')
    def test_form_invalid_doesnt_set_skippable_true_when_generic_validation_error_is_raised(self,
            get_form, get_context_data, render_to_response):
        # setup
        view = AddEmployeeQuestionnaireFromSignUpFormView()
        form = mock.Mock()
        get_form.return_value.clean.configure_mock(
            side_effect=forms.ValidationError(''))

        # action
        response = view.form_invalid(form)

        # assert
        self.assertDictEqual(dict(skippable=False, form=form),
            get_context_data.call_args[1])

    def get_request(self):
        request = mock.Mock()
        request.path = reverse('employee:questionnaire_signup_add')
        request.META.get = mock.Mock(return_value='')
        request.POST = {}
        return request
