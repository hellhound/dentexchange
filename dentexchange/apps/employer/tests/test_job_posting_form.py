# -*- coding:utf-8 -*-
import unittest
import mock

from django import forms

from employee import constants as employee_constants
from ..forms import JobPostingForm
from .. import strings, constants


class JobPostingFormTestCase(unittest.TestCase):
    def setUp(self):
        self.cleaned_data = dict(
            ### General Info
            position_name='Position Name',
            posting_title='Posting Title',
            ### Job Position you're offering
            job_position=\
                employee_constants.JOB_POSITION_CHOICES.JOB_POSITION_1,
            ### Type of schedule required
            schedule_type=\
                employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME,
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
            compensation_type=\
                employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY,
            hourly_wage=\
                employee_constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_1,
            annualy_wage=None,
            ### Experience required
            experience_years=\
                employee_constants.EXPERIENCE_YEARS_CHOICES.EXPERIENCE_1,
            ### Benefits being offered
            benefit_1=False,
            benefit_2=False,
            benefit_3=False,
            benefit_4=False,
            benefit_5=False,
            benefit_6=False,
            benefit_other=False,
            benefit_other_text='Some other benefit',
            ### Additional Comments
            additional_comments='Some comments',
        )

    def test_init_should_assign_praxis_pk_and_is_posted(self):
        # setup
        praxis = mock.Mock()
        is_posted = True

        # action
        form = JobPostingForm(praxis=praxis, is_posted=is_posted)

        # assert
        self.assertEqual(id(praxis), id(form.praxis))
        self.assertEqual(id(is_posted), id(form.is_posted))

    def test_clean_should_return_cleaned_data(self):
        # setup
        form = JobPostingForm()
        form.cleaned_data = self.cleaned_data

        # action
        cleaned_data = form.clean()

        # assert
        self.assertDictEqual(self.cleaned_data, cleaned_data)

    def test_clean_should_raise_validation_error_exception_when_form_is_incomplete(
            self):
        # setup
        form = JobPostingForm()
        self.cleaned_data['position_name'] = None
        form.cleaned_data = self.cleaned_data

        # action
        with self.assertRaises(forms.ValidationError) as cm:
            form.clean()

        # assert
        self.assertEqual(strings.JOB_POSTING_FORM_INCOMPLETE_FORM_ERROR,
            cm.exception.message)

    @mock.patch('employer.forms.forms.ModelForm.clean')
    def test_clean_should_remove_hourly_wage_from_cleaned_data_when_compensation_type_is_salary(
            self, clean):
        # setup
        form = JobPostingForm()
        self.cleaned_data['compensation_type'] = \
            employee_constants.COMPENSATION_TYPE_CHOICES.SALARY
        self.cleaned_data['annualy_wage'] = \
            employee_constants.ANNUALY_WAGE_CHOICES.ANNUALY_WAGE_1
        cleaned_data = mock.MagicMock()
        cleaned_data.copy = mock.Mock(return_value=self.cleaned_data)
        cleaned_data.__getitem__ = mock.MagicMock(
            side_effect=self.cleaned_data.__getitem__)
        form.cleaned_data = cleaned_data

        # action
        form.clean()

        # assert
        self.assertNotIn('hourly_wage', self.cleaned_data)

    @mock.patch('employer.forms.forms.ModelForm.clean')
    def test_clean_should_remove_annualy_wage_from_cleaned_data_when_compensation_type_is_hourly(
            self, clean):
        # setup
        form = JobPostingForm()
        self.cleaned_data['compensation_type'] = \
            employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY
        self.cleaned_data['hourly_wage'] = \
            employee_constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_1
        cleaned_data = mock.MagicMock()
        cleaned_data.copy = mock.Mock(return_value=self.cleaned_data)
        cleaned_data.__getitem__ = mock.MagicMock(
            side_effect=self.cleaned_data.__getitem__)
        form.cleaned_data = cleaned_data

        # action
        form.clean()

        # assert
        self.assertNotIn('annualy_wage', self.cleaned_data)

    @mock.patch('employer.forms.Praxis.objects.get')
    @mock.patch('employer.forms.forms.ModelForm.save')
    def test_save_should_save_and_return_job_posting(self, save, get):
        # setup
        form = JobPostingForm()
        form.instance = mock.Mock()
        form.cleaned_data = self.cleaned_data
        instance = save.return_value

        # action
        returned_value = form.save(commit=True)
        
        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertEqual(1, save.call_count)
        self.assertEqual(id(instance), id(returned_value))

    @mock.patch('employer.forms.forms.ModelForm.save')
    def test_save_should_assign_praxis_to_instance_save_it_then_return_it(self,
            save):
        # setup
        praxis = mock.Mock()
        form = JobPostingForm(praxis=praxis)
        form.cleaned_data = self.cleaned_data
        instance = save.return_value

        # ation
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertTrue(id(form.praxis), id(instance.praxis))
        self.assertTrue(1, instance.save.call_count)
        self.assertTrue(id(instance), id(returned_value))

    @mock.patch('employer.forms.Praxis.objects.get')
    @mock.patch('employer.forms.forms.ModelForm.save')
    def test_save_should_assign_is_posted_to_instance(
            self, save, get):
        # setup
        is_posted = True
        form = JobPostingForm(is_posted=is_posted)
        form.cleaned_data = self.cleaned_data
        instance = save.return_value

        # ation
        returned_value = form.save()

        # assert
        self.assertDictEqual(dict(commit=False), save.call_args[1])
        self.assertTrue(id(form.is_posted), id(instance.is_posted))
        self.assertTrue(1, instance.save.call_count)
        self.assertTrue(id(instance), id(returned_value))

    @mock.patch('employer.forms.forms.ModelForm.save')
    def test_save_should_clean_schedule_days_selections_when_schedule_type_is_full_time(self,
            save):
        # setup
        user = mock.Mock()
        form = JobPostingForm()
        self.cleaned_data['schedule_type'] = \
            employee_constants.SCHEDULE_TYPE_CHOICES.FULL_TIME
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

    @mock.patch('employer.forms.forms.ModelForm.save')
    def test_save_should_clean_hourly_wage_when_compensation_type_is_salary(
            self, save):
        # setup
        user = mock.Mock()
        form = JobPostingForm()
        self.cleaned_data['compensation_type'] = \
            employee_constants.COMPENSATION_TYPE_CHOICES.SALARY
        self.cleaned_data['hourly_wage'] = \
            employee_constants.HOURLY_WAGE_CHOICES.HOURLY_WAGE_1
        form.cleaned_data = self.cleaned_data

        # action
        form.save()

        # assert
        self.assertIsNone(self.cleaned_data['hourly_wage'])

    @mock.patch('employer.forms.forms.ModelForm.save')
    def test_save_should_clean_annualy_wage_when_compensation_type_is_hourly(
            self, save):
        # setup
        user = mock.Mock()
        form = JobPostingForm()
        self.cleaned_data['compensation_type'] = \
            employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY
        self.cleaned_data['annualy_wage'] = \
            employee_constants.ANNUALY_WAGE_CHOICES.ANNUALY_WAGE_1
        form.cleaned_data = self.cleaned_data

        # action
        form.save()

        # assert
        self.assertIsNone(self.cleaned_data['annualy_wage'])
