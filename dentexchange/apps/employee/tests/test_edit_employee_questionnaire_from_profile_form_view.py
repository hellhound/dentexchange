# -*- coding:utf-8 -*-
import unittest
import mock

from django.core.urlresolvers import reverse
from django import forms

from ..views import EditEmployeeQuestionnaireFromProfileFormView
from ..models import EmployeeQuestionnaire
from .. import constants


class EditEmployeeQuestionnaireFromProfileFormViewTestCase(unittest.TestCase):
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_get_should_call_render_to_response_with_questionnaire_form(
            self, resume_form):
        # setup
        view = EditEmployeeQuestionnaireFromProfileFormView()
        view.render_to_response = mock.Mock()
        request = self.get_request()
        view.request = request
        view.get_object = mock.Mock(return_value=EmployeeQuestionnaire())
        view.kwargs = dict(pk=1)

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
        view = EditEmployeeQuestionnaireFromProfileFormView()
        request = self.get_request()
        view.request = request
        view.response_class = mock.Mock()
        view.get_object = mock.Mock(return_value=EmployeeQuestionnaire())
        view.kwargs = dict(pk=1)
        template_name = \
            'employee/add_edit_employee_questionnaire_form.html'

        # action
        view.get(request)

        # assert
        self.assertEqual(1, view.response_class.call_count)
        self.assertEqual(template_name,
            view.response_class.call_args[1]['template'][0])

    def test_form_valid_should_redirect_to_success_url(self):
        # setup
        view = EditEmployeeQuestionnaireFromProfileFormView()

        # assert
        self.assertEqual('employee:dashboard', view.success_url_alias)

    def get_request(self):
        request = mock.Mock()
        request.path = reverse('employee:questionnaire_edit', args=(1,))
        request.META.get = mock.Mock(return_value='')
        return request
