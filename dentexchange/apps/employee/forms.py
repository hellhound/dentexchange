# -*- coding:utf-8 -*-
from django import forms

from ajax_upload.widgets import AjaxClearableFileInput
from validatedfile.fields import QuotaValidator

from libs.mixins.forms import (MeaningfulEmptyValueFormMixin,
    UserInitializationFormMixin)
from libs import constants as lib_constants
from registration.models import UserRegistration
from .models import EmployeeQuestionnaire, Resume
from . import strings, constants


class ResumeForm(forms.ModelForm):
    class Meta(object):
        model = Resume
        widgets = dict(cv_file=AjaxClearableFileInput)

    class Media(object):
        css = dict(
            all=('ajax_upload/css/ajax-upload-widget.css',)
        )
        js = (
            'ajax_upload/js/jquery.iframe-transport.js',
            'ajax_upload/js/ajax-upload-widget.js',
            'employee/js/resume_ajax_upload_discovery.js'
        )

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['cv_file'].validators = [
            QuotaValidator(max_usage=constants.RESUME_CV_FILE_CONTENT_TYPES),
        ]


class ResumeForQuestionnaireForm(UserInitializationFormMixin, ResumeForm):
    class Meta(ResumeForm.Meta):
        exclude = ('user',)


class EmployeeQuestionnaireForm(MeaningfulEmptyValueFormMixin,
        UserInitializationFormMixin, forms.ModelForm):
    ### Personal Info
    first_name = forms.CharField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_FIRST_NAME,
        max_length=100, required=False)
    last_name = forms.CharField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_LAST_NAME,
        max_length=100, required=False)
    personal_address = forms.CharField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_PERSONAL_ADDRESS,
        max_length=200, required=False)
    personal_zip_code = forms.DecimalField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_ZIP_CODE,
        max_digits=5, decimal_places=0, required=False,
        widget=forms.TextInput)
    personal_city = forms.CharField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_CITY,
        max_length=100, required=False)
    personal_state = forms.ChoiceField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_STATE,
        choices=lib_constants.STATE_CHOICES,
        required=False)
    ## Location
    zip_code = forms.DecimalField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_ZIP_CODE,
        max_digits=5, decimal_places=0, required=False,
        widget=forms.TextInput)
    ### Type of schedule required
    schedule_type = forms.TypedChoiceField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_SCHEDULE_TYPE,
        choices=constants.SCHEDULE_TYPE_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect)
    ### Compensation
    compensation_type = forms.TypedChoiceField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_COMPENSATION_TYPE,
        choices=constants.COMPENSATION_TYPE_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect)
    ### Visa
    visa = forms.TypedChoiceField(
        label=strings.EMPLOYEE_QUESTIONNAIRE_VISA,
        choices=lib_constants.YES_NO_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect)
    non_meaningful_fields = ('schedule_type', 'compensation_type', 'visa')

    class Meta(object):
        model = EmployeeQuestionnaire
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(EmployeeQuestionnaireForm, self).__init__(*args, **kwargs)
        self.init_personal_info_fields()
        kwargs = kwargs.copy()
        kwargs['instance'] = self.get_resume()
        kwargs['user'] = self.user
        self.resume_form = ResumeForQuestionnaireForm(*args, **kwargs)

    def get_resume(self):
        if self.user is None:
            return None
        try:
            return self.user.resume
        except Resume.DoesNotExist:
            return None

    def init_personal_info_fields(self):
        if self.user is not None:
            user_registration = self.user.userregistration
            self.fields['first_name'].initial = user_registration.first_name
            self.fields['last_name'].initial = user_registration.last_name
            self.fields['personal_address'].initial = \
                user_registration.personal_address
            self.fields['personal_zip_code'].initial = \
                user_registration.personal_zip_code
            self.fields['personal_city'].initial = \
                user_registration.personal_city
            self.fields['personal_state'].initial = \
                user_registration.personal_state

    def is_valid(self):
        resume_is_valid = self.resume_form.is_valid()
        return super(EmployeeQuestionnaireForm, self).is_valid() \
            and ((self.resume_form.cleaned_data.get('cv_file') is None \
            and resume_is_valid) or resume_is_valid)

    def save(self, commit=True):
        data = self.cleaned_data
        if data['schedule_type'] == constants.SCHEDULE_TYPE_CHOICES.FULL_TIME:
            for key, value in data.iteritems():
                if key.endswith('_daytime') or key.endswith('_evening'):
                    data[key] = False
        if data['compensation_type'] == \
                constants.COMPENSATION_TYPE_CHOICES.SALARY:
            data['hourly_wage'] = None
        else:
            data['annualy_wage'] = None
        questionnaire = super(EmployeeQuestionnaireForm, self).save(
            commit=commit)
        self._save_personal_info(questionnaire)
        self.resume_form.save(commit=commit)
        return questionnaire

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


class EmployeeQuestionnaireSignUpForm(EmployeeQuestionnaireForm):
    def __init__(self, skippable=False, *args, **kwargs):
        super(EmployeeQuestionnaireSignUpForm, self).__init__(*args, **kwargs)
        self.skippable = skippable

    def _clean_all_fields_filled(self):
        data = self.cleaned_data.copy()
        compensation_type = data.get('compensation_type',
            self.initial['compensation_type'])
        if compensation_type  == \
                constants.COMPENSATION_TYPE_CHOICES.HOURLY:
            data.pop('annualy_wage')
        else:
            data.pop('hourly_wage')
        values = [value for key, value in data.iteritems()
            if not (key in ('schedule_type', 'compensation_type') \
            or isinstance(self.fields[key], forms.BooleanField))]
        is_incomplete_form = any(
            map(
                lambda v: v is None or (
                    isinstance(v, basestring) and v.strip() == ''),
                values))
        if is_incomplete_form:
            raise forms.ValidationError(
                strings.QUESTIONNAIRE_FORM_INCOMPLETE_FORM_ERROR,
                code=constants.QUESTIONNAIRE_FORM_INCOMPLETE_FORM_ERROR_CODE)

    def clean(self):
        if not self.skippable:
            self._clean_all_fields_filled()
        return super(EmployeeQuestionnaireSignUpForm, self).clean()
