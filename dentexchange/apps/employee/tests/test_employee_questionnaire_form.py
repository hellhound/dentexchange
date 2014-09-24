# -*- coding:utf-8 -*-
import unittest
import mock

from django import forms

from ..forms import EmployeeQuestionnaireForm
from .. import constants, strings
from libs import constants as lib_constants


class EmployeeQuestionnaireFormTestCase(unittest.TestCase):
    def setUp(self):
        self.initial = dict(
            schedule_type=constants.SCHEDULE_TYPE_CHOICES.PART_TIME, 
            compensation_type=constants.COMPENSATION_TYPE_CHOICES.HOURLY,
            visa=lib_constants.YES_NO_CHOICES.YES,
            )
        self.cleaned_data = dict(
            ### Personal Info
            first_name='First Name',
            last_name='Last Name',
            personal_address='123 Address',
            personal_zip_code=12345,
            personal_city='City',
            personal_state='State',
            ### Job Position you're looking for
            job_position=constants.JOB_POSITION_CHOICES.JOB_POSITION_1,
            ### Type of Practice
            solo_practitioner=True,
            multi_practitioner=False,
            corporate=True,
            ### Patients' Method of Payment
            fee_for_service=False,
            insurance=True,
            capitation_medicaid=False,
            ### Location
            zip_code=54321,
            city='Location City',
            state='Location State',
            distance=constants.DISTANCE_CHOICES.DISTANCE_1,
            ### Type of schedule required
            schedule_type=constants.SCHEDULE_TYPE_CHOICES.PART_TIME,
            monday_daytime=True,
            monday_evening=False,
            tuesday_daytime=False,
            tuesday_evening=True,
            wednesday_daytime=True,
            wednesday_evening=False,
            thursday_daytime=False,
            thursday_evening=True,
            friday_daytime=True,
            friday_evening=False,
            saturday_daytime=False,
            saturday_evening=True,
            sunday_daytime=True,
            sunday_evening=False,
            ### Compensation
            compensation_type=constants.COMPENSATION_TYPE_CHOICES.HOURLY,
            hourly_wage=constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_1,
            annualy_wage=None,
            ### Experience
            experience_years=constants.EXPERIENCE_YEARS_CHOICES.EXPERIENCE_1,
            ### Education
            dental_school='Dental School',
            graduation_year=constants.GRADUATION_YEAR_CHOICES.YEAR_1,
            ### Specific strengths
            specific_strengths='Specific strengths')
        self.init_personal_info_fields = \
            EmployeeQuestionnaireForm.init_personal_info_fields

    def tearDown(self):
        EmployeeQuestionnaireForm.init_personal_info_fields = \
            self.init_personal_info_fields

    @mock.patch('employee.forms.UserInitializationFormMixin.save')
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_save_should_save_and_return_questionnaire(self, resume_form, save):
        # setup
        user = mock.Mock()
        form = EmployeeQuestionnaireForm(user=user)
        form.instance = mock.Mock()
        form.cleaned_data = self.cleaned_data
        questionnaire = save.return_value

        # action
        returned_value = form.save(commit=True)
        
        # assert
        self.assertDictEqual(dict(commit=True), save.call_args[1])
        self.assertEqual(1, save.call_count)
        self.assertEqual(id(questionnaire), id(returned_value))

    @mock.patch('employee.forms.UserInitializationFormMixin.save')
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_save_should_clean_schedule_days_selections_when_schedule_type_is_full_time(
            self, resume_form, save):
        # setup
        user = mock.Mock()
        form = EmployeeQuestionnaireForm(user=user)
        self.cleaned_data['schedule_type'] = \
            constants.SCHEDULE_TYPE_CHOICES.FULL_TIME
        form.cleaned_data = self.cleaned_data

        # action
        form.save()

        # assert
        self.assertDictContainsSubset(dict(
            monday_daytime=False,
            monday_evening=False,
            tuesday_daytime=False,
            tuesday_evening=False,
            wednesday_daytime=False,
            wednesday_evening=False,
            thursday_daytime=False,
            thursday_evening=False,
            friday_daytime=False,
            friday_evening=False,
            saturday_daytime=False,
            saturday_evening=False,
            sunday_daytime=False,
            sunday_evening=False), self.cleaned_data)

    @mock.patch('employee.forms.UserInitializationFormMixin.save')
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_save_should_clean_hourly_wage_when_compensation_type_is_salary(
            self, resume_form, save):
        # setup
        user = mock.Mock()
        form = EmployeeQuestionnaireForm(user=user)
        self.cleaned_data['compensation_type'] = \
            constants.COMPENSATION_TYPE_CHOICES.SALARY
        self.cleaned_data['hourly_wage'] = \
            constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_1
        form.cleaned_data = self.cleaned_data

        # action
        form.save()

        # assert
        self.assertEqual(None, self.cleaned_data['hourly_wage'])

    @mock.patch('employee.forms.UserInitializationFormMixin.save')
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_save_should_clean_annualy_wage_when_compensation_type_is_hourly(
            self, resume_form, save):
        # setup
        user = mock.Mock()
        form = EmployeeQuestionnaireForm(user=user)
        self.cleaned_data['compensation_type'] = \
            constants.COMPENSATION_TYPE_CHOICES.HOURLY
        self.cleaned_data['annualy_wage'] = \
            constants.ANNUALY_WAGE_CHOICES.ANNUALY_WAGE_1
        form.cleaned_data = self.cleaned_data

        # action
        form.save()

        # assert
        self.assertEqual(None, self.cleaned_data['annualy_wage'])

    @mock.patch('employee.forms.UserInitializationFormMixin.save')
    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_save_should_save_personal_info_fields(self, resume_form, save):
        # setup
        user = mock.Mock()
        instance = mock.Mock()
        instance.user = user
        user_registration = mock.Mock()
        user.configure_mock(userregistration=user_registration)
        form = EmployeeQuestionnaireForm(user=user)
        form.cleaned_data = self.cleaned_data
        save.return_value = instance

        # action
        form.save()

        # assert
        self.assertEqual(self.cleaned_data['first_name'],
            user_registration.first_name)
        self.assertEqual(self.cleaned_data['last_name'],
            user_registration.last_name)
        self.assertEqual(self.cleaned_data['personal_address'],
            user_registration.personal_address)
        self.assertEqual(self.cleaned_data['personal_zip_code'],
            user_registration.personal_zip_code)
        self.assertEqual(self.cleaned_data['personal_city'],
            user_registration.personal_city)
        self.assertEqual(self.cleaned_data['personal_state'],
            user_registration.personal_state)
        self.assertEqual(1, user_registration.save.call_count)

    @mock.patch('employee.forms.ResumeForQuestionnaireForm')
    def test_init_should_call_init_personal_info_fields(self, resume_form):
        # setup
        EmployeeQuestionnaireForm.init_personal_info_fields = mock.Mock()
        user = mock.Mock()

        # action
        form = EmployeeQuestionnaireForm(user=user)

        # assert
        self.assertEqual(1, form.init_personal_info_fields.call_count)

    def test_init_personal_info_fields(self):
        # setup
        form = EmployeeQuestionnaireForm()
        user = mock.Mock()
        form.user = user

        # action
        form.init_personal_info_fields()

        # assert
        self.assertEqual(id(user.userregistration.first_name),
            id(form.fields['first_name'].initial))
        self.assertEqual(id(user.userregistration.last_name),
            id(form.fields['last_name'].initial))
        self.assertEqual(id(user.userregistration.personal_address),
            id(form.fields['personal_address'].initial))
        self.assertEqual(id(user.userregistration.personal_zip_code),
            id(form.fields['personal_zip_code'].initial))
        self.assertEqual(id(user.userregistration.personal_city),
            id(form.fields['personal_city'].initial))
        self.assertEqual(id(user.userregistration.personal_state),
            id(form.fields['personal_state'].initial))
