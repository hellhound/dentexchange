# -*- coding:utf-8 -*-
from django import forms

from libs.mixins.forms import (MeaningfulEmptyValueFormMixin,
    UserInitializationFormMixin)
from libs import constants as lib_constants
from employee import constants as employee_constants
from .models import Business, Praxis, JobPosting
from . import strings, constants


class BusinessForm(MeaningfulEmptyValueFormMixin,
        UserInitializationFormMixin, forms.ModelForm):
    is_mso = forms.TypedChoiceField(label=strings.BUSINESS_IS_MSO,
        choices=lib_constants.YES_NO_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect)
    ### Personal Info
    first_name = forms.CharField(
        label=strings.BUSINESS_FIRST_NAME,
        max_length=100, required=False)
    last_name = forms.CharField(
        label=strings.BUSINESS_LAST_NAME,
        max_length=100, required=False)
    personal_address = forms.CharField(
        label=strings.BUSINESS_PERSONAL_ADDRESS,
        max_length=200, required=False)
    personal_zip_code = forms.DecimalField(
        label=strings.BUSINESS_ZIP_CODE,
        max_digits=5, decimal_places=0, required=False,
        widget=forms.TextInput)
    personal_city = forms.CharField(
        label=strings.BUSINESS_CITY,
        max_length=100, required=False)
    personal_state = forms.ChoiceField(
        label=strings.BUSINESS_STATE,
        choices=lib_constants.STATE_CHOICES,
        required=False)
    non_meaningful_fields = ('is_mso',)

    class Meta(object):
        model = Business
        exclude = ('user',)

    def _save_personal_info(self, instance):
        data = self.cleaned_data
        user = instance.user
        user_registration = user.userregistration
        user_registration.first_name = data['first_name']
        user_registration.last_name = data['last_name']
        user_registration.personal_address = data['personal_address']
        user_registration.personal_zip_code = data['personal_zip_code']
        user_registration.personal_city = data['personal_city']
        user_registration.personal_state = data['personal_state']
        user_registration.save()

    def save(self, commit=True):
        instance = super(BusinessForm, self).save(commit=commit)
        self._save_personal_info(instance)
        return instance


class PraxisForm(MeaningfulEmptyValueFormMixin,
        UserInitializationFormMixin, forms.ModelForm):
    zip_code = forms.DecimalField(
        label=strings.PRAXIS_ZIP_CODE,
        max_digits=5, decimal_places=0,
        widget=forms.TextInput)

    class Meta(object):
        model = Praxis
        exclude = ('business', 'is_active',)

    def save(self, commit=True):
        instance = super(PraxisForm, self).save(commit=False)
        instance.business = self.user.business
        instance.save()
        return instance


class JobPostingForm(MeaningfulEmptyValueFormMixin, forms.ModelForm):
    ### Type of schedule required
    schedule_type = forms.TypedChoiceField(
        label=strings.JOB_POSTING_SCHEDULE_TYPE,
        choices=employee_constants.SCHEDULE_TYPE_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect)
    ### Compensation
    compensation_type = forms.TypedChoiceField(
        label=strings.JOB_POSTING_COMPENSATION_TYPE,
        choices=employee_constants.COMPENSATION_TYPE_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect)
    non_meaningful_fields = ('schedule_type', 'compensation_type', 'visa')

    class Meta(object):
        model = JobPosting
        exclude = ('praxis', 'is_posted', 'is_active',)

    def __init__(self, praxis=None, is_posted=False, *args, **kwargs):
        super(JobPostingForm, self).__init__(*args, **kwargs)
        self.praxis = praxis
        self.is_posted = is_posted

    def save(self, commit=False):
        data = self.cleaned_data
        if data['schedule_type'] == \
                employee_constants.SCHEDULE_TYPE_CHOICES.FULL_TIME:
            for key, value in data.iteritems():
                if key.endswith('_daytime') or key.endswith('_evening'):
                    data[key] = False
        if data['compensation_type'] == \
                employee_constants.COMPENSATION_TYPE_CHOICES.SALARY:
            data['hourly_wage'] = None
        else:
            data['annualy_wage'] = None
        instance = super(JobPostingForm, self).save(commit=False)
        instance.praxis = self.praxis
        instance.is_posted = self.is_posted
        instance.save()
        return instance

    def _clean_all_fields_filled(self):
        data = self.cleaned_data.copy()
        if data['compensation_type'] == \
                employee_constants.COMPENSATION_TYPE_CHOICES.HOURLY:
            data.pop('annualy_wage')
        else:
            data.pop('hourly_wage')
        values = [value for key, value in data.iteritems()
            if not (key in (
                'schedule_type', 'compensation_type', 'benefit_other_text',
                'additional_comments') \
            or isinstance(self.fields[key], forms.BooleanField))]
        is_incomplete_form = any(
            map(
                lambda v: v is None or (
                    isinstance(v, basestring) and v.strip() == ''),
                values))
        if is_incomplete_form:
            raise forms.ValidationError(
                strings.JOB_POSTING_FORM_INCOMPLETE_FORM_ERROR,
                code=constants.JOB_POSTING_FORM_INCOMPLETE_FORM_ERROR_CODE)

    def clean(self):
        self._clean_all_fields_filled()
        return super(JobPostingForm, self).clean()
